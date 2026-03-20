import { test, expect } from "@playwright/test";

test.describe("Field Monitor Dashboard", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/field-monitor");
    await expect(
      page.locator('select option:not([value=""])').first(),
    ).toBeAttached({ timeout: 10000 });
  });

  test("loads and shows title", async ({ page }) => {
    await expect(
      page.getByRole("heading", { name: "Field Monitor Dashboard" }),
    ).toBeVisible();
  });

  test("shows Moat badge", async ({ page }) => {
    await expect(page.getByText("Moat")).toBeVisible();
  });

  test("township dropdown is present and populated", async ({ page }) => {
    const select = page.locator("select");
    await expect(select).toBeVisible();
    await expect(select.locator('option[value=""]')).toBeAttached();
    const optionCount = await select.locator("option").count();
    expect(optionCount).toBeGreaterThan(1);
  });

  test("monitor button is disabled when no township selected", async ({
    page,
  }) => {
    const monitorBtn = page.getByRole("button", { name: "Monitor" });
    await expect(monitorBtn).toBeDisabled();
  });

  test("monitor button enables after selecting a township", async ({
    page,
  }) => {
    const monitorBtn = page.getByRole("button", { name: "Monitor" });
    await expect(monitorBtn).toBeDisabled();
    await page.locator("select").selectOption({ index: 1 });
    await expect(monitorBtn).toBeEnabled();
  });

  test("sidebar navigation to /field-monitor works", async ({ page }) => {
    await page.goto("/dashboard");
    await page.getByTestId("nav-field-monitor").click();
    await page.waitForURL("**/field-monitor");
    await expect(
      page.getByRole("heading", { name: "Field Monitor Dashboard" }),
    ).toBeVisible();
  });
});
