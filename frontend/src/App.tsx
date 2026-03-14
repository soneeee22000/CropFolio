import { useReducer } from "react";
import { Header } from "@/components/layout/Header";
import { ErrorBoundary } from "@/components/common/ErrorBoundary";
import { TownshipSelector } from "@/components/township/TownshipSelector";
import { ClimateRiskDashboard } from "@/components/climate/ClimateRiskDashboard";
import { PortfolioOptimizer } from "@/components/optimizer/PortfolioOptimizer";
import { MonteCarloView } from "@/components/simulator/MonteCarloView";
import type { OptimizeResponse } from "@/types/optimizer";

interface AppState {
  currentStep: number;
  townshipId: string | null;
  season: "monsoon" | "dry";
  optimizeResult: OptimizeResponse | null;
}

type AppAction =
  | { type: "SELECT_TOWNSHIP"; townshipId: string; season: "monsoon" | "dry" }
  | { type: "GO_TO_STEP"; step: number }
  | { type: "SET_OPTIMIZE_RESULT"; result: OptimizeResponse };

const initialState: AppState = {
  currentStep: 0,
  townshipId: null,
  season: "monsoon",
  optimizeResult: null,
};

/** App state reducer for wizard flow. */
function reducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case "SELECT_TOWNSHIP":
      return {
        ...state,
        townshipId: action.townshipId,
        season: action.season,
        currentStep: 1,
        optimizeResult: null,
      };
    case "GO_TO_STEP":
      return { ...state, currentStep: action.step };
    case "SET_OPTIMIZE_RESULT":
      return {
        ...state,
        optimizeResult: action.result,
        currentStep: 3,
      };
    default:
      return state;
  }
}

/** Root application component with step-based wizard flow. */
export default function App() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div className="min-h-screen bg-surface">
      <Header currentStep={state.currentStep} />

      <main className="max-w-7xl mx-auto px-6 py-16">
        {state.currentStep > 0 && (
          <button
            onClick={() =>
              dispatch({ type: "GO_TO_STEP", step: state.currentStep - 1 })
            }
            className="mb-8 text-sm text-text-tertiary hover:text-text-primary transition-colors duration-200 animate-fade-in-up"
          >
            &larr; Back
          </button>
        )}

        <ErrorBoundary>
          <div key={state.currentStep} className="animate-fade-in-up">
            {state.currentStep === 0 && (
              <TownshipSelector
                onSelect={(townshipId, season) =>
                  dispatch({ type: "SELECT_TOWNSHIP", townshipId, season })
                }
              />
            )}

            {state.currentStep === 1 && state.townshipId && (
              <ClimateRiskDashboard
                townshipId={state.townshipId}
                season={state.season}
                onContinue={() => dispatch({ type: "GO_TO_STEP", step: 2 })}
              />
            )}

            {state.currentStep === 2 && state.townshipId && (
              <PortfolioOptimizer
                townshipId={state.townshipId}
                season={state.season}
                onComplete={(result) =>
                  dispatch({ type: "SET_OPTIMIZE_RESULT", result })
                }
              />
            )}

            {state.currentStep === 3 &&
              state.townshipId &&
              state.optimizeResult && (
                <MonteCarloView
                  townshipId={state.townshipId}
                  season={state.season}
                  optimizeResult={state.optimizeResult}
                />
              )}
          </div>
        </ErrorBoundary>
      </main>

      <footer className="mt-24 border-t border-border py-8 text-center">
        <p className="font-display text-lg text-text-primary">CropFolio</p>
        <p className="text-xs text-text-tertiary mt-1">
          Portfolio Theory for Climate-Resilient Farming
        </p>
      </footer>
    </div>
  );
}
