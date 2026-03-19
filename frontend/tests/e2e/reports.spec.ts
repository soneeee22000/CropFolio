import { test, expect } from "@playwright/test";

test.describe("Reports Page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/reports");
  });

  test("renders report generator interface", async ({ page }) => {
    await expect(
      page.getByRole("heading", { name: "Reports", exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Advisory Report Generator" }),
    ).toBeVisible();
  });

  test("has language toggle buttons", async ({ page }) => {
    await expect(page.getByTestId("btn-pdf-en")).toBeVisible();
    await expect(page.getByTestId("btn-pdf-mm")).toBeVisible();
  });

  test("Burmese is default language", async ({ page }) => {
    const mmBtn = page.getByTestId("btn-pdf-mm");
    await expect(mmBtn).toHaveClass(/bg-primary/);

    // Download button should say Burmese
    await expect(page.getByTestId("btn-download-pdf")).toContainText("Burmese");
  });

  test("toggles to English and back", async ({ page }) => {
    // Switch to English
    await page.getByTestId("btn-pdf-en").click();
    await expect(page.getByTestId("btn-pdf-en")).toHaveClass(/bg-primary/);
    await expect(page.getByTestId("btn-download-pdf")).toContainText("English");

    // Switch back to Burmese
    await page.getByTestId("btn-pdf-mm").click();
    await expect(page.getByTestId("btn-pdf-mm")).toHaveClass(/bg-primary/);
    await expect(page.getByTestId("btn-download-pdf")).toContainText("Burmese");
  });

  test("download button triggers PDF generation", async ({ page }) => {
    // Intercept the PDF request
    const downloadPromise = page.waitForEvent("download", { timeout: 30000 });

    await page.getByTestId("btn-download-pdf").click();

    // Wait for download to start
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toContain("cropfolio-report");
  });
});
