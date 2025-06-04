import {createFileRoute, redirect} from '@tanstack/react-router'
import {ChartBarLabelCustom} from "@/widgets/statistic/chart_bar_custom.tsx";

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
		<>
			<ChartBarLabelCustom />
		</>

	)
}
