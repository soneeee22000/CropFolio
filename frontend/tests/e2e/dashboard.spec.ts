import { test, expect } from "@playwright/test";

test.describe("Dashboard Overview", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/dashboard");
  });

  test("loads and displays KPI cards", async ({ page }) => {
    const kpiGrid = page.getByTestId("kpi-cards");
    await expect(kpiGrid).toBeVisible();

    // Should show 50 townships, 11 crops, 8 fertilizers
    await expect(kpiGrid.getByText("50")).toBeVisible({ timeout: 10000 });
    await expect(kpiGrid.getByText("11")).toBeVisible();
    await expect(kpiGrid.getByText("8")).toBeVisible();
    await expect(kpiGrid.getByText("1,000")).toBeVisible();
  });

  test("quick action navigates to recommend page", async ({ page }) => {
    await page.getByTestId("btn-generate-rec").click();
    await page.waitForURL("**/recommend");
    await expect(page.getByTestId("recommend-page")).toBeVisible();
  });

  test("quick action navigates to demo ROI page", async ({ page }) => {
    await page.getByTestId("btn-demo-roi").click();
    await page.waitForURL("**/demo-calculator");
    await expect(page.getByTestId("demo-roi-page")).toBeVisible();
  });

  test("sidebar navigation works", async ({ page }) => {
    // Navigate to Recommend
    await page.getByTestId("nav-recommend").click();
    await page.waitForURL("**/recommend");
    await expect(page.getByTestId("recommend-page")).toBeVisible();

    // Navigate to Demo ROI
    await page.getByTestId("nav-demo-calculator").click();
    await page.waitForURL("**/demo-calculator");
    await expect(page.getByTestId("demo-roi-page")).toBeVisible();

    // Navigate to Reports
    await page.getByTestId("nav-reports").click();
    await page.waitForURL("**/reports");
    await expect(page.getByText("Advisory Report Generator")).toBeVisible();

    // Navigate back to Dashboard
    await page.getByTestId("nav-dashboard").click();
    await page.waitForURL("**/dashboard");
    await expect(page.getByTestId("dashboard-overview")).toBeVisible();
  });

  test("displays coverage by region", async ({ page }) => {
    await expect(page.getByText("Mandalay")).toBeVisible({ timeout: 10000 });
    await expect(page.getByText("Sagaing")).toBeVisible();
    await expect(page.getByText("Ayeyarwady")).toBeVisible();
  });
});
