import { useEffect, useRef } from "react";
import * as d3 from "d3";
import type { HistogramBin, SimulationStats } from "@/types/simulator";
import { formatMMKCompact } from "@/utils/formatters";
import { ANIMATION_DURATION_MS, STAGGER_DELAY_MS } from "@/constants";

interface MonteCarloHistogramProps {
  histogram: HistogramBin[];
  stats: SimulationStats;
  comparisonHistogram?: HistogramBin[];
}

const MARGIN = { top: 20, right: 30, bottom: 50, left: 70 };
const PRIMARY_COLOR = "#16a34a";
const COMPARISON_COLOR = "#ef4444";

/** D3-powered animated histogram for Monte Carlo income distribution. */
export function MonteCarloHistogram({
  histogram,
  stats,
  comparisonHistogram,
}: MonteCarloHistogramProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!svgRef.current || !containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = 350;
    const innerW = width - MARGIN.left - MARGIN.right;
    const innerH = height - MARGIN.top - MARGIN.bottom;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();
    svg.attr("width", width).attr("height", height);

    const g = svg
      .append("g")
      .attr("transform", `translate(${MARGIN.left},${MARGIN.top})`);

    const xScale = d3
      .scaleLinear()
      .domain([histogram[0].bin_start, histogram[histogram.length - 1].bin_end])
      .range([0, innerW]);

    const maxFreq = d3.max(histogram, (d) => d.frequency) ?? 0.1;
    const compMaxFreq = comparisonHistogram
      ? (d3.max(comparisonHistogram, (d) => d.frequency) ?? 0)
      : 0;

    const yScale = d3
      .scaleLinear()
      .domain([0, Math.max(maxFreq, compMaxFreq) * 1.15])
      .range([innerH, 0]);

    // X axis
    g.append("g")
      .attr("transform", `translate(0,${innerH})`)
      .call(
        d3
          .axisBottom(xScale)
          .ticks(6)
          .tickFormat((d) => formatMMKCompact(d as number)),
      )
      .selectAll("text")
      .attr("transform", "rotate(-20)")
      .style("text-anchor", "end")
      .style("font-size", "11px");

    // Y axis
    g.append("g")
      .call(d3.axisLeft(yScale).ticks(5).tickFormat(d3.format(".0%")))
      .selectAll("text")
      .style("font-size", "11px");

    // X label
    g.append("text")
      .attr("x", innerW / 2)
      .attr("y", innerH + 45)
      .attr("text-anchor", "middle")
      .style("font-size", "12px")
      .style("fill", "#6b7280")
      .text("Income per Hectare (MMK)");

    // Y label
    g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -innerH / 2)
      .attr("y", -55)
      .attr("text-anchor", "middle")
      .style("font-size", "12px")
      .style("fill", "#6b7280")
      .text("Frequency");

    // Animated bars
    const barWidth = innerW / histogram.length - 1;

    g.selectAll(".bar")
      .data(histogram)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", (d) => xScale(d.bin_start))
      .attr("width", Math.max(barWidth, 1))
      .attr("y", innerH)
      .attr("height", 0)
      .attr("fill", PRIMARY_COLOR)
      .attr("opacity", 0.8)
      .attr("rx", 1)
      .transition()
      .duration(ANIMATION_DURATION_MS)
      .delay((_, i) => i * STAGGER_DELAY_MS)
      .ease(d3.easeCubicOut)
      .attr("y", (d) => yScale(d.frequency))
      .attr("height", (d) => innerH - yScale(d.frequency));

    // Mean line (appears after bars)
    const meanDelay =
      ANIMATION_DURATION_MS + histogram.length * STAGGER_DELAY_MS;

    g.append("line")
      .attr("x1", xScale(stats.mean_income))
      .attr("x2", xScale(stats.mean_income))
      .attr("y1", 0)
      .attr("y2", innerH)
      .attr("stroke", "#1e293b")
      .attr("stroke-width", 2)
      .attr("stroke-dasharray", "6,3")
      .attr("opacity", 0)
      .transition()
      .delay(meanDelay)
      .duration(400)
      .attr("opacity", 1);

    g.append("text")
      .attr("x", xScale(stats.mean_income) + 5)
      .attr("y", 12)
      .style("font-size", "11px")
      .style("font-weight", "600")
      .style("fill", "#1e293b")
      .attr("opacity", 0)
      .text(`Mean: ${formatMMKCompact(stats.mean_income)}`)
      .transition()
      .delay(meanDelay)
      .duration(400)
      .attr("opacity", 1);

    // 5th-95th percentile shading
    g.append("rect")
      .attr("x", xScale(stats.percentile_5))
      .attr("width", xScale(stats.percentile_95) - xScale(stats.percentile_5))
      .attr("y", 0)
      .attr("height", innerH)
      .attr("fill", PRIMARY_COLOR)
      .attr("opacity", 0)
      .transition()
      .delay(meanDelay + 200)
      .duration(400)
      .attr("opacity", 0.06);

    // Comparison overlay (monocrop)
    if (comparisonHistogram) {
      const compDelay = meanDelay + 600;
      const compBarWidth = innerW / comparisonHistogram.length - 1;

      g.selectAll(".comp-bar")
        .data(comparisonHistogram)
        .enter()
        .append("rect")
        .attr("class", "comp-bar")
        .attr("x", (d) => xScale(d.bin_start))
        .attr("width", Math.max(compBarWidth, 1))
        .attr("y", (d) => yScale(d.frequency))
        .attr("height", (d) => innerH - yScale(d.frequency))
        .attr("fill", "none")
        .attr("stroke", COMPARISON_COLOR)
        .attr("stroke-width", 1.5)
        .attr("opacity", 0)
        .transition()
        .delay(compDelay)
        .duration(600)
        .attr("opacity", 0.7);

      // Legend
      const legend = g
        .append("g")
        .attr("transform", `translate(${innerW - 160}, 5)`);

      legend
        .append("rect")
        .attr("width", 12)
        .attr("height", 12)
        .attr("fill", PRIMARY_COLOR)
        .attr("opacity", 0.8);
      legend
        .append("text")
        .attr("x", 16)
        .attr("y", 10)
        .style("font-size", "11px")
        .text("Diversified");

      legend
        .append("rect")
        .attr("y", 18)
        .attr("width", 12)
        .attr("height", 12)
        .attr("fill", "none")
        .attr("stroke", COMPARISON_COLOR)
        .attr("stroke-width", 1.5);
      legend
        .append("text")
        .attr("x", 16)
        .attr("y", 28)
        .style("font-size", "11px")
        .text("Monocrop (Rice)");
    }
  }, [histogram, stats, comparisonHistogram]);

  return (
    <div ref={containerRef} className="w-full">
      <svg ref={svgRef} className="w-full" />
    </div>
  );
}
