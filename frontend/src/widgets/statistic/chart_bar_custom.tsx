"use client"

import {Bar, BarChart, CartesianGrid, LabelList, XAxis, YAxis} from "recharts"

import {Card, CardContent, CardHeader, CardTitle,} from "@/shared/components/ui/card"
import {ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent,} from "@/shared/components/ui/chart"
import {useAuth} from "@/shared/providers/auth.provider.tsx";
import {$api} from "@/shared/api/new_api.ts";


const chartConfig = {
	desktop: {
		label: "Desktop",
		color: "var(--chart-2)",
	},
	mobile: {
		label: "Mobile",
		color: "var(--chart-2)",
	},
	label: {
		color: "var(--background)",
	},
} satisfies ChartConfig

export function ChartBarLabelCustom() {

	const {user} = useAuth()

	const {data} = $api.useQuery(
		"get",
		"/statistic/top_films",
		{
			params: {
				query: {
					user_id: user?.sub
				}
			}
		}
	)

	const mapped_data = data?.map((item) => {
		return {
			title: item.title,
			rating: item.rating,
		}
	})

	return (
		<Card className={"w-1/2"}>
			<CardHeader>
				<CardTitle>Топ 10 фильмов юзера - { user?.username }</CardTitle>
			</CardHeader>
			<CardContent>
				<ChartContainer config={chartConfig}>
					<BarChart
						accessibilityLayer
						data={mapped_data}
						layout="vertical"
						margin={{
							right: 16,
						}}
					>
						<CartesianGrid horizontal={false} />
						<YAxis
							dataKey="title"
							type="category"
							tickLine={false}
							tickMargin={10}
							axisLine={false}
							tickFormatter={(value) => value.slice(0, 3)}
							hide
						/>
						<XAxis dataKey="rating" type="number" hide />
						<ChartTooltip
							cursor={false}
							content={<ChartTooltipContent indicator="line" />}
						/>
						<Bar
							dataKey="rating"
							layout="vertical"
							fill="var(--color-desktop)"
							radius={4}
						>
							<LabelList
								dataKey="title"
								position="insideLeft"
								offset={8}
								className="fill-(--color-label)"
								fontSize={12}
							/>
							<LabelList
								dataKey="rating"
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
	)
}
