import { test, expect } from "@playwright/test";

test.describe("Recommendation Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/recommend");
    // Wait for townships and crops to load
    await expect(page.getByTestId("township-mdy_meiktila")).toBeVisible({
      timeout: 10000,
    });
  });

  test("shows township and crop selectors", async ({ page }) => {
    // Townships should be grouped by region
    await expect(page.getByText("Mandalay").first()).toBeVisible();
    await expect(page.getByTestId("township-mdy_meiktila")).toBeVisible();
    await expect(page.getByTestId("township-mgw_magway")).toBeVisible();

    // Crops should be visible
    await expect(page.getByTestId("crop-rice")).toBeVisible();
    await expect(page.getByTestId("crop-black_gram")).toBeVisible();
  });

  test("submit button disabled until valid selection", async ({ page }) => {
    const submitBtn = page.getByTestId("btn-recommend");
    await expect(submitBtn).toBeDisabled();

    // Select 1 township — still disabled (need >= 2 crops)
    await page.getByTestId("township-mdy_meiktila").click();
    await expect(submitBtn).toBeDisabled();

    // Select 1 crop — still disabled
    await page.getByTestId("crop-rice").click();
    await expect(submitBtn).toBeDisabled();

    // Select 2nd crop — now enabled
    await page.getByTestId("crop-black_gram").click();
    await expect(submitBtn).toBeEnabled();
  });

  test("generates recommendation for Meiktila with 3 crops", async ({
    page,
  }) => {
    // Select Meiktila
    await page.getByTestId("township-mdy_meiktila").click();

    // Select 3 priced crops
    await page.getByTestId("crop-rice").click();
    await page.getByTestId("crop-black_gram").click();
    await page.getByTestId("crop-sesame").click();

    // Set season to dry
    await page.getByTestId("season-dry").click();

    // Submit
    await page.getByTestId("btn-recommend").click();

    // Wait for results
    const results = page.getByTestId("recommend-results");
    await expect(results).toBeVisible({ timeout: 30000 });

    // Should show Meiktila township name
    await expect(results.getByText("Meiktila")).toBeVisible();

    // Should show crop allocation cards
    await expect(results.getByRole("heading", { name: /Rice/ })).toBeVisible();

    // Should show soil profile
    await expect(results.getByText(/loam/i).first()).toBeVisible();
  });

  test("generates recommendation for multiple townships", async ({ page }) => {
    // Select 2 townships
    await page.getByTestId("township-mdy_meiktila").click();
    await page.getByTestId("township-mgw_magway").click();

    // Select crops
    await page.getByTestId("crop-rice").click();
    await page.getByTestId("crop-chickpea").click();

    // Submit
    await page.getByTestId("btn-recommend").click();

    // Wait for results
    const results = page.getByTestId("recommend-results");
    await expect(results).toBeVisible({ timeout: 30000 });

    // Both townships should appear
    await expect(results.getByText("Meiktila")).toBeVisible();
    await expect(results.getByText("Magway")).toBeVisible();
  });

  test("risk slider adjusts tolerance value", async ({ page }) => {
    const slider = page.getByTestId("risk-slider");
    await expect(slider).toBeVisible();

    // Default should show 50%
    await expect(page.getByText("50%")).toBeVisible();
  });

  test("season toggle switches between dry and monsoon", async ({ page }) => {
    const dryBtn = page.getByTestId("season-dry");
    const monsoonBtn = page.getByTestId("season-monsoon");

    // Dry should be selected by default
    await expect(dryBtn).toHaveClass(/border-primary/);

    // Click monsoon
    await monsoonBtn.click();
    await expect(monsoonBtn).toHaveClass(/border-primary/);
  });
});
