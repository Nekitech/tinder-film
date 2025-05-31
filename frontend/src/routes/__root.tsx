import * as React from 'react'
import {createRootRoute, Outlet} from '@tanstack/react-router'
import {TanStackRouterDevtools} from '@tanstack/react-router-devtools'
import {ThemeProvider} from "@/shared/providers/theme.provider.tsx";

export const Route = createRootRoute({
	component: RootComponent,
})

function RootComponent() {
	return (
		<React.Fragment>
			<ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
				<Outlet />
			</ThemeProvider>
			<TanStackRouterDevtools />
		</React.Fragment>
	)
}
