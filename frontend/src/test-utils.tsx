import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { LanguageProvider } from "./i18n/LanguageContext";

/** Wraps children with all required providers for testing. */
function AllProviders({ children }: { children: React.ReactNode }) {
  return (
    <LanguageProvider>
      <BrowserRouter>{children}</BrowserRouter>
    </LanguageProvider>
  );
}

/** Custom render that wraps UI in all app providers. */
function customRender(
  ui: React.ReactElement,
  options?: Parameters<typeof render>[1],
) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export { customRender as render };
export { screen, waitFor } from "@testing-library/react";
