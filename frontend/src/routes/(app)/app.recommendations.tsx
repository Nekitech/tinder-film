import {createFileRoute, redirect} from '@tanstack/react-router'
import TinderCards from "@/widgets/tinder_cards.tsx";

export const Route = createFileRoute('/(app)/app/recommendations')({
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
	return <TinderCards />
}
