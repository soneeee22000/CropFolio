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
    <div className="min-h-screen bg-gray-50">
      <Header currentStep={state.currentStep} />

      <main className="max-w-6xl mx-auto px-4 py-8">
        {state.currentStep > 0 && (
          <button
            onClick={() =>
              dispatch({ type: "GO_TO_STEP", step: state.currentStep - 1 })
            }
            className="mb-6 text-sm text-gray-500 hover:text-gray-700 transition-colors"
          >
            &larr; Back
          </button>
        )}

        <ErrorBoundary>
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
        </ErrorBoundary>
      </main>

      <footer className="text-center py-4 text-xs text-gray-400 border-t border-gray-200">
        CropFolio — AI for Climate-Resilient Agriculture | Hackathon 2026
      </footer>
    </div>
  );
}
