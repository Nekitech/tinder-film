import {useAuth} from "@/shared/providers/auth.provider.tsx";
import {$api} from "@/shared/api/new_api.ts";
import {ChartBarLabelCustom} from "@/widgets/statistic/chart_bar_custom.tsx";
import {Spinner} from "@/shared/components/ui/spinner.tsx";

export const UserTopMoviesChart: React.FC = () => {
	const {user} = useAuth();

	const {data, isPending} = $api.useQuery(
		"get",
		"/statistic/top_films",
		{
			params: {
				query: {
					user_id: Number(user?.sub)
				}
			}
		}
	);

	const mappedData = data?.map((item) => ({
		title: item.title,
		rating: item.rating
	}));

	const chartConfig = {
		desktop: {
			label: "Desktop",
			color: "var(--chart-2)"
		},
		mobile: {
			label: "Mobile",
			color: "var(--chart-2)"
		},
		label: {
			color: "var(--background)"
		}
	};

	if (isPending) {
		return <Spinner size={"large"} />;
	}

	return (
		<ChartBarLabelCustom
			data={mappedData || []}
			title={`Топ 10 фильмов юзера - ${user?.username}`}
			chartConfig={chartConfig}
			barColor="var(--color-desktop)"
			xAxisKey="rating"
			yAxisKey="title"
			xAxisType="number"
			yAxisType="category"

		/>
	);
};