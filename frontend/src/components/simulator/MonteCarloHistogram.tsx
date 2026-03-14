import { useEffect, useRef } from "react";
import * as d3 from "d3";
import type { HistogramBin, SimulationStats } from "@/types/simulator";
import { formatMMKCompact } from "@/utils/formatters";
import { ANIMATION_DURATION_MS, STAGGER_DELAY_MS } from "@/constants";
import { useResizeObserver } from "@/hooks/useResizeObserver";

interface MonteCarloHistogramProps {
  histogram: HistogramBin[];
  stats: SimulationStats;
  comparisonHistogram?: HistogramBin[];
}

const MARGIN = { top: 40, right: 40, bottom: 60, left: 80 };
const PRIMARY_COLOR = "#1B7A4A";
const COMPARISON_COLOR = "#C43B3B";
const TEXT_PRIMARY = "#1A1A18";
const TEXT_TERTIARY = "#A3A29D";
const BORDER_COLOR = "#E8E6E1";
const SURFACE_SUBTLE = "#F5F4F0";

/** Gallery-quality D3 histogram for Monte Carlo income distribution. */
export function MonteCarloHistogram({
  histogram,
  stats,
  comparisonHistogram,
}: MonteCarloHistogramProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const { ref: containerRef, width } = useResizeObserver();

  useEffect(() => {
    if (!svgRef.current || !width) return;
    const height = 420;
    const innerW = width - MARGIN.left - MARGIN.right;
    const innerH = height - MARGIN.top - MARGIN.bottom;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();
    svg.attr("width", width).attr("height", height);

    const g = svg
      .append("g")
      .attr("transform", `translate(${MARGIN.left},${MARGIN.top})`);

    // Chart background
    g.append("rect")
      .attr("width", innerW)
      .attr("height", innerH)
      .attr("fill", SURFACE_SUBTLE)
      .attr("rx", 4);

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

    // Horizontal grid lines
    const yTicks = yScale.ticks(5);
    g.selectAll(".grid-line")
      .data(yTicks)
      .enter()
      .append("line")
      .attr("x1", 0)
      .attr("x2", innerW)
      .attr("y1", (d) => yScale(d))
      .attr("y2", (d) => yScale(d))
      .attr("stroke", BORDER_COLOR)
      .attr("stroke-opacity", 0.4)
      .attr("stroke-dasharray", "2,4");

    // X axis
    g.append("g")
      .attr("transform", `translate(0,${innerH})`)
      .call(
        d3
          .axisBottom(xScale)
          .ticks(4)
          .tickFormat((d) => formatMMKCompact(d as number)),
      )
      .call((axis) => axis.select(".domain").remove())
      .selectAll("text")
      .style("font-family", '"JetBrains Mono", monospace')
      .style("font-size", "12px")
      .style("fill", TEXT_TERTIARY);

    // Y axis
    g.append("g")
      .call(d3.axisLeft(yScale).ticks(5).tickFormat(d3.format(".0%")))
      .call((axis) => axis.select(".domain").remove())
      .selectAll("text")
      .style("font-family", '"JetBrains Mono", monospace')
      .style("font-size", "12px")
      .style("fill", TEXT_TERTIARY);

    // Remove tick lines
    g.selectAll(".tick line").attr("stroke", "none");

    // X label
    g.append("text")
      .attr("x", innerW / 2)
      .attr("y", innerH + 48)
      .attr("text-anchor", "middle")
      .style("font-family", '"DM Sans", sans-serif')
      .style("font-size", "13px")
      .style("fill", TEXT_TERTIARY)
      .text("Income per Hectare (MMK)");

    // Y label
    g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -innerH / 2)
      .attr("y", -60)
      .attr("text-anchor", "middle")
      .style("font-family", '"DM Sans", sans-serif')
      .style("font-size", "13px")
      .style("fill", TEXT_TERTIARY)
      .text("Frequency");

    // Animated bars
    const barWidth = innerW / histogram.length - 2;

    g.selectAll(".bar")
      .data(histogram)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", (d) => xScale(d.bin_start) + 1)
      .attr("width", Math.max(barWidth, 1))
      .attr("y", innerH)
      .attr("height", 0)
      .attr("fill", PRIMARY_COLOR)
      .transition()
      .duration(ANIMATION_DURATION_MS)
      .delay((_, i) => i * STAGGER_DELAY_MS)
      .ease(d3.easeBackOut.overshoot(0.3))
      .attr("y", (d) => yScale(d.frequency))
      .attr("height", (d) => innerH - yScale(d.frequency));

    // Mean line with tag (appears after bars)
    const meanDelay =
      ANIMATION_DURATION_MS + histogram.length * STAGGER_DELAY_MS;

    g.append("line")
      .attr("x1", xScale(stats.mean_income))
      .attr("x2", xScale(stats.mean_income))
      .attr("y1", 0)
      .attr("y2", innerH)
      .attr("stroke", TEXT_PRIMARY)
      .attr("stroke-width", 1.5)
      .attr("opacity", 0)
      .transition()
      .delay(meanDelay)
      .duration(400)
      .attr("opacity", 1);

    // Mean tag
    const tagWidth = 110;
    const tagHeight = 22;
    const tagX = Math.min(
      xScale(stats.mean_income) - tagWidth / 2,
      innerW - tagWidth,
    );

    const meanTag = g
      .append("g")
      .attr("transform", `translate(${tagX}, -4)`)
      .attr("opacity", 0);

    meanTag
      .append("rect")
      .attr("width", tagWidth)
      .attr("height", tagHeight)
      .attr("rx", 4)
      .attr("fill", TEXT_PRIMARY);

    meanTag
      .append("text")
      .attr("x", tagWidth / 2)
      .attr("y", tagHeight / 2 + 4)
      .attr("text-anchor", "middle")
      .style("font-family", '"JetBrains Mono", monospace')
      .style("font-size", "11px")
      .style("font-weight", "500")
      .style("fill", "#FFFFFF")
      .text(`Mean: ${formatMMKCompact(stats.mean_income)}`);

    meanTag.transition().delay(meanDelay).duration(400).attr("opacity", 1);

    // 5th-95th percentile band
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

    // P5 / P95 labels
    [
      { val: stats.percentile_5, label: "P5" },
      { val: stats.percentile_95, label: "P95" },
    ].forEach(({ val, label }) => {
      g.append("line")
        .attr("x1", xScale(val))
        .attr("x2", xScale(val))
        .attr("y1", 0)
        .attr("y2", innerH)
        .attr("stroke", TEXT_PRIMARY)
        .attr("stroke-width", 1)
        .attr("stroke-opacity", 0.2)
        .attr("opacity", 0)
        .transition()
        .delay(meanDelay + 300)
        .duration(300)
        .attr("opacity", 1);

      g.append("text")
        .attr("x", xScale(val))
        .attr("y", innerH + 18)
        .attr("text-anchor", "middle")
        .style("font-family", '"JetBrains Mono", monospace')
        .style("font-size", "10px")
        .style("fill", TEXT_TERTIARY)
        .attr("opacity", 0)
        .text(label)
        .transition()
        .delay(meanDelay + 300)
        .duration(300)
        .attr("opacity", 1);
    });

    // Comparison overlay — smooth curve
    if (comparisonHistogram && comparisonHistogram.length >= 3) {
      const compDelay = meanDelay + 600;
      const points = comparisonHistogram.map((d) => ({
        x: (d.bin_start + d.bin_end) / 2,
        y: d.frequency,
      }));

      const lineGen = d3
        .line<{ x: number; y: number }>()
        .x((d) => xScale(d.x))
        .y((d) => yScale(d.y))
        .curve(d3.curveBasis);

      const path = g
        .append("path")
        .datum(points)
        .attr("d", lineGen)
        .attr("fill", "none")
        .attr("stroke", COMPARISON_COLOR)
        .attr("stroke-width", 2.5)
        .attr("stroke-opacity", 0.8);

      const pathLength = path.node()?.getTotalLength() ?? 0;
      path
        .attr("stroke-dasharray", pathLength)
        .attr("stroke-dashoffset", pathLength)
        .transition()
        .delay(compDelay)
        .duration(1000)
        .ease(d3.easeQuadOut)
        .attr("stroke-dashoffset", 0);

      // Legend
      const legend = g
        .append("g")
        .attr("transform", `translate(${innerW - 140}, 12)`);

      legend
        .append("rect")
        .attr("width", 14)
        .attr("height", 10)
        .attr("fill", PRIMARY_COLOR)
        .attr("rx", 1);
      legend
        .append("text")
        .attr("x", 20)
        .attr("y", 9)
        .style("font-family", '"DM Sans", sans-serif')
        .style("font-size", "11px")
        .style("fill", TEXT_TERTIARY)
        .text("Diversified");

      legend
        .append("line")
        .attr("x1", 0)
        .attr("x2", 14)
        .attr("y1", 24)
        .attr("y2", 24)
        .attr("stroke", COMPARISON_COLOR)
        .attr("stroke-width", 2.5);
      legend
        .append("text")
        .attr("x", 20)
        .attr("y", 28)
        .style("font-family", '"DM Sans", sans-serif')
        .style("font-size", "11px")
        .style("fill", TEXT_TERTIARY)
        .text("Monocrop (Rice)");
    }
  }, [histogram, stats, comparisonHistogram, width]);

  return (
    <div ref={containerRef} className="w-full">
      <svg ref={svgRef} className="w-full" />
    </div>
  );
}
