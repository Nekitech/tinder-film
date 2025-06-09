import {createFileRoute, redirect} from '@tanstack/react-router'
import {UserTopMoviesChart} from "@/widgets/statistic/user_top_movies_chart.tsx";
import {UserTopGenreChart} from "@/widgets/statistic/user_top_genre_chart.tsx";

export const Route = createFileRoute('/(app)/app/statistics')({
	component: RouteComponent,
	beforeLoad: ({context, location}) => {
		const auth = context.auth.isAuthenticated
		if (auth && !auth()) {
			throw redirect({
				to: '/login',
				search: {
					redirect: location.href,
				},
			})
		}
	},
})

function RouteComponent() {
	return (
		<div className={"flex flex-col gap-4 py-4"}>
			<UserTopMoviesChart />
			<UserTopGenreChart />
		</div>

	)
}
