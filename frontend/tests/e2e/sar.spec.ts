import { test, expect } from "@playwright/test";

test.describe("SAR Planting Verification", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/sar");
    // Wait for townships to populate the dropdown before interacting
    await expect(
      page.locator('select option:not([value=""])').first(),
    ).toBeAttached({ timeout: 10000 });
  });

  test("loads and shows title", async ({ page }) => {
    await expect(
      page.getByRole("heading", { name: "SAR Planting Verification" }),
    ).toBeVisible();
  });

  test("shows Beta badge", async ({ page }) => {
    await expect(page.getByText("Beta")).toBeVisible();
  });

  test("township dropdown is present and populated", async ({ page }) => {
    const select = page.locator("select");
    await expect(select).toBeVisible();

    // Placeholder option must be present
    await expect(select.locator('option[value=""]')).toBeAttached();

    // At least one real township option must be loaded
    const optionCount = await select.locator("option").count();
    expect(optionCount).toBeGreaterThan(1);
  });

  test("season toggle works between monsoon and dry", async ({ page }) => {
    const monsoonBtn = page.getByRole("button", { name: "Monsoon" });
    const dryBtn = page.getByRole("button", { name: "Dry" });

    await expect(monsoonBtn).toBeVisible();
    await expect(dryBtn).toBeVisible();

    // Default season is monsoon — reflected by border-primary class
    await expect(monsoonBtn).toHaveClass(/border-primary/);

    // Switch to dry
    await dryBtn.click();
    await expect(dryBtn).toHaveClass(/border-primary/);
    await expect(monsoonBtn).not.toHaveClass(/border-primary/);

    // Switch back to monsoon
    await monsoonBtn.click();
    await expect(monsoonBtn).toHaveClass(/border-primary/);
  });

  test("analyze button is disabled when no township is selected", async ({
    page,
  }) => {
    const analyzeBtn = page.getByRole("button", { name: "Analyze" });
    await expect(analyzeBtn).toBeDisabled();
  });

  test("analyze button enables after selecting a township", async ({
    page,
  }) => {
    const analyzeBtn = page.getByRole("button", { name: "Analyze" });

    // Button is initially disabled
    await expect(analyzeBtn).toBeDisabled();

    // Select the first real township option
    await page.locator("select").selectOption({ index: 1 });

    await expect(analyzeBtn).toBeEnabled();
  });

  test("sidebar navigation to /sar works", async ({ page }) => {
    // Start from the dashboard then navigate to SAR via sidebar
    await page.goto("/dashboard");
    await page.getByTestId("nav-sar").click();
    await page.waitForURL("**/sar");
    await expect(
      page.getByRole("heading", { name: "SAR Planting Verification" }),
    ).toBeVisible();
  });
});
