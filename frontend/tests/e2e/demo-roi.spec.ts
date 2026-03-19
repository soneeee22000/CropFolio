import { test, expect } from "@playwright/test";

test.describe("Demo ROI Calculator", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/demo-calculator");
    // Wait for dropdowns to populate
    await expect(page.getByTestId("select-township")).toBeVisible({
      timeout: 10000,
    });
  });

  test("shows input form with all fields", async ({ page }) => {
    await expect(page.getByTestId("select-township")).toBeVisible();
    await expect(page.getByTestId("select-crop")).toBeVisible();
    await expect(page.getByTestId("input-area")).toBeVisible();
    await expect(page.getByTestId("btn-calculate")).toBeVisible();
  });

  test("calculate button disabled until township and crop selected", async ({
    page,
  }) => {
    await expect(page.getByTestId("btn-calculate")).toBeDisabled();

    // Select township
    await page.getByTestId("select-township").selectOption("mdy_meiktila");
    await expect(page.getByTestId("btn-calculate")).toBeDisabled();

    // Select crop
    await page.getByTestId("select-crop").selectOption("rice");
    await expect(page.getByTestId("btn-calculate")).toBeEnabled();
  });

  test("calculates ROI for rice in Meiktila", async ({ page }) => {
    // Fill form
    await page.getByTestId("select-township").selectOption("mdy_meiktila");
    await page.getByTestId("select-crop").selectOption("rice");
    await page.getByTestId("input-area").fill("2");

    // Calculate
    await page.getByTestId("btn-calculate").click();

    // Wait for results
    const results = page.getByTestId("roi-results");
    await expect(results).toBeVisible({ timeout: 30000 });

    // Should show crop name and township in heading
    await expect(
      results.getByRole("heading", { name: /Rice.*Meiktila/ }),
    ).toBeVisible();

    // Should show financial metrics
    await expect(results.getByText(/Total Input Cost/i)).toBeVisible();

    // Should show success probability
    await expect(results.getByText(/Success/i).first()).toBeVisible();
  });

  test("shows soil profile in results", async ({ page }) => {
    await page.getByTestId("select-township").selectOption("mdy_meiktila");
    await page.getByTestId("select-crop").selectOption("rice");
    await page.getByTestId("btn-calculate").click();

    const results = page.getByTestId("roi-results");
    await expect(results).toBeVisible({ timeout: 30000 });

    // Meiktila has soil data — should show soil profile card
    await expect(results.getByText(/loam/i)).toBeVisible();
  });

  test("shows fertilizer recommendation in results", async ({ page }) => {
    await page.getByTestId("select-township").selectOption("mdy_meiktila");
    await page.getByTestId("select-crop").selectOption("rice");
    await page.getByTestId("btn-calculate").click();

    const results = page.getByTestId("roi-results");
    await expect(results).toBeVisible({ timeout: 30000 });

    // Should show recommended fertilizer with formulation
    await expect(results.getByText(/kg\/ha/).first()).toBeVisible();
  });

  test("handles crop with zero price gracefully", async ({ page }) => {
    await page.getByTestId("select-township").selectOption("mdy_meiktila");
    await page.getByTestId("select-crop").selectOption("maize");
    await page.getByTestId("btn-calculate").click();

    // Should still show results (revenue will be 0)
    const results = page.getByTestId("roi-results");
    await expect(results).toBeVisible({ timeout: 30000 });
    await expect(results.getByRole("heading", { name: /Maize/ })).toBeVisible();
  });
});
