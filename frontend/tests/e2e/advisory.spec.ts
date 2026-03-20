import { test, expect } from "@playwright/test";

test.describe("Advisory Page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/advisory");
  });

  test("page loads with title visible", async ({ page }) => {
    const title = page.getByTestId("advisory-title");
    await expect(title).toBeVisible();
    await expect(title).toHaveText(/AI Advisory/);
  });

  test("township dropdown is populated", async ({ page }) => {
    const select = page.getByTestId("advisory-township-select");
    await expect(select).toBeVisible();
    await expect(select.locator("option")).not.toHaveCount(1, {
      timeout: 10000,
    });
    const options = await select.locator("option").count();
    expect(options).toBeGreaterThan(1);
  });

  test("generate button is disabled until township selected", async ({
    page,
  }) => {
    const btn = page.getByTestId("advisory-generate-btn");
    await expect(btn).toBeDisabled();

    const select = page.getByTestId("advisory-township-select");
    await select.selectOption({ index: 1 });
    await expect(btn).toBeEnabled();
  });

  test("query input is present", async ({ page }) => {
    const input = page.getByPlaceholder(/ask a question/i);
    await expect(input).toBeVisible();
  });

  test("sidebar navigation works", async ({ page }) => {
    const navLink = page.getByTestId("nav-advisory");
    await expect(navLink).toBeVisible();
  });
});
