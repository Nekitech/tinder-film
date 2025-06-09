"use client";

import {Bar, BarChart, CartesianGrid, LabelList, XAxis, YAxis} from "recharts";

import {Card, CardContent, CardHeader, CardTitle} from "@/shared/components/ui/card";
import {ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent} from "@/shared/components/ui/chart";

interface ChartBarLabelCustomProps {
    data: Array<Record<string, any>>; // Данные для отображения (обобщённый тип)
    title: string; // Название графика
    chartConfig: ChartConfig; // Конфигурация графика (опционально)
    barColor?: string; // Цвет "баров"
    xAxisKey: string; // dataKey для X оси
    yAxisKey: string; // dataKey для Y оси
    xAxisType?: "number" | "category"; // Тип X оси
    yAxisType?: "number" | "category"; // Тип Y оси
}

export const ChartBarLabelCustom: React.FC<ChartBarLabelCustomProps> = ({
	data,
	title,
	chartConfig,
	barColor = "var(--chart-2)",
	xAxisKey,
	yAxisKey,
	xAxisType = "number",
	yAxisType = "category"
}) => {
	return (
		<Card className={"w-1/2"}>
			<CardHeader>
				<CardTitle>{ title }</CardTitle>
			</CardHeader>
			<CardContent>
				<ChartContainer config={chartConfig}>
					<BarChart
						accessibilityLayer
						data={data}
						layout="vertical"
						margin={{
							right: 16
						}}
					>
						<CartesianGrid horizontal={false} />
						<YAxis
							dataKey={yAxisKey}
							type={yAxisType}
							tickLine={false}
							tickMargin={10}
							axisLine={false}
							tickFormatter={(value) => value}
							hide={false} // Можно также позволить передавать `hide` как пропс, если нужно
						/>
						<XAxis
							dataKey={xAxisKey}
							type={xAxisType}
							hide={false} // Аналогично
						/>
						<ChartTooltip
							cursor={false}
							content={<ChartTooltipContent indicator="line" />}
						/>
						<Bar
							dataKey={xAxisKey}
							layout="vertical"
							fill={barColor}
							radius={4}
						>
							<LabelList
								dataKey={yAxisKey}
								position="insideLeft"
								offset={8}
								className="fill-(--color-label)"
								fontSize={12}
							/>
							<LabelList
								dataKey={xAxisKey}
								position="right"
								offset={8}
								className="fill-foreground"
								fontSize={12}
							/>
						</Bar>
					</BarChart>
				</ChartContainer>
			</CardContent>
		</Card>
	);
};