import { test, expect } from "@playwright/test";

test.describe("Landing Page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("renders hero section with CropFolio branding", async ({ page }) => {
    await expect(page.locator("text=CropFolio").first()).toBeVisible();
    await expect(
      page.getByRole("link", { name: /Launch CropFolio Pro/i }),
    ).toBeVisible();
  });

  test("navigates to dashboard via CTA button", async ({ page }) => {
    await page.getByRole("link", { name: /Launch CropFolio Pro/i }).click();
    await page.waitForURL("**/dashboard");
    await expect(page.getByTestId("dashboard-overview")).toBeVisible();
  });

  test("hackathon attribution is visible", async ({ page }) => {
    await expect(
      page.getByText("AI for Climate-Resilient Agriculture Hackathon 2026"),
    ).toBeVisible();
  });
});
