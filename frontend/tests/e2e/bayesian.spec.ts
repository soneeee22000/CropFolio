import { test, expect } from "@playwright/test";

test.describe("Bayesian Analyzer", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/bayesian");
    // Wait for townships to populate the dropdown — the placeholder option is
    // always present immediately; we wait for at least one real option to appear
    // so the select is usable before interacting with it.
    await expect(
      page.locator('select option:not([value=""])').first(),
    ).toBeAttached({ timeout: 10000 });
  });

  test("loads and shows title", async ({ page }) => {
    await expect(
      page.getByRole("heading", { name: "Bayesian Analyzer" }),
    ).toBeVisible();
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

  test("crop selection buttons are visible", async ({ page }) => {
    // Crops are rendered as buttons inside the setup card.
    // Wait for at least one crop button to appear after async load.
    const cropButtons = page.locator(
      'button:not([disabled]):not(:has-text("Dry")):not(:has-text("Monsoon")):not(:has-text("Run Bayesian Analysis"))',
    );
    await expect(cropButtons.first()).toBeVisible({ timeout: 10000 });

    // The app ships 11 crop profiles — verify a meaningful number are rendered.
    const count = await page.locator(".flex.flex-wrap.gap-2 button").count();
    expect(count).toBeGreaterThanOrEqual(2);
  });

  test("season toggle works between dry and monsoon", async ({ page }) => {
    const dryBtn = page.getByRole("button", { name: "Dry" });
    const monsoonBtn = page.getByRole("button", { name: "Monsoon" });

    await expect(dryBtn).toBeVisible();
    await expect(monsoonBtn).toBeVisible();

    // Default season is dry — button reflects active state via border-primary
    await expect(dryBtn).toHaveClass(/border-primary/);

    // Switch to monsoon
    await monsoonBtn.click();
    await expect(monsoonBtn).toHaveClass(/border-primary/);
    await expect(dryBtn).not.toHaveClass(/border-primary/);

    // Switch back to dry
    await dryBtn.click();
    await expect(dryBtn).toHaveClass(/border-primary/);
  });

  test("evidence panel has 4 evidence options", async ({ page }) => {
    await expect(page.getByText("Observed Rainfall")).toBeVisible();
    await expect(page.getByText("Drought Observed")).toBeVisible();
    await expect(page.getByText("Flood Observed")).toBeVisible();
    await expect(page.getByText("Soil Quality")).toBeVisible();
  });

  test("evidence toggle buttons are clickable and show active state", async ({
    page,
  }) => {
    // Click the "normal" rainfall value button
    const normalBtn = page.getByRole("button", { name: "normal" });
    await expect(normalBtn).toBeVisible();
    await normalBtn.click();
    // Active state uses border-accent class
    await expect(normalBtn).toHaveClass(/border-accent/);

    // Clicking the same value again deactivates it
    await normalBtn.click();
    await expect(normalBtn).not.toHaveClass(/border-accent/);

    // Click a drought evidence button
    const yesButtons = page.getByRole("button", { name: "yes" });
    await yesButtons.first().click();
    await expect(yesButtons.first()).toHaveClass(/border-accent/);
  });

  test("submit button is disabled when no township is selected", async ({
    page,
  }) => {
    const submitBtn = page.getByRole("button", {
      name: "Run Bayesian Analysis",
    });
    await expect(submitBtn).toBeDisabled();
  });

  test("submit button is disabled with township but fewer than 2 crops", async ({
    page,
  }) => {
    const submitBtn = page.getByRole("button", {
      name: "Run Bayesian Analysis",
    });

    // Select a township
    await page.locator("select").selectOption({ index: 1 });
    await expect(submitBtn).toBeDisabled();

    // Select exactly 1 crop
    const cropButtons = page.locator(".flex.flex-wrap.gap-2 button");
    await cropButtons.first().click();
    await expect(submitBtn).toBeDisabled();
  });

  test("submit button enables with township and 2 or more crops", async ({
    page,
  }) => {
    const submitBtn = page.getByRole("button", {
      name: "Run Bayesian Analysis",
    });

    // Select a township
    await page.locator("select").selectOption({ index: 1 });

    // Select 2 crops
    const cropButtons = page.locator(".flex.flex-wrap.gap-2 button");
    await cropButtons.nth(0).click();
    await cropButtons.nth(1).click();

    await expect(submitBtn).toBeEnabled();
  });

  test("sidebar navigation to /bayesian works", async ({ page }) => {
    // Start from the dashboard then navigate back to bayesian via sidebar
    await page.goto("/dashboard");
    await page.getByTestId("nav-bayesian").click();
    await page.waitForURL("**/bayesian");
    await expect(
      page.getByRole("heading", { name: "Bayesian Analyzer" }),
    ).toBeVisible();
  });
});
