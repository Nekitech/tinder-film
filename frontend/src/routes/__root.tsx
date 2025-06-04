import * as React from 'react'
import {createRootRouteWithContext, Outlet} from '@tanstack/react-router'
import {TanStackRouterDevtools} from '@tanstack/react-router-devtools'
import {ThemeProvider} from "@/shared/providers/theme.provider.tsx";
import {AuthContextType} from "@/shared/providers/auth.provider.tsx";

interface MyRouterContext {
    auth: AuthContextType
}

export const Route = createRootRouteWithContext<MyRouterContext>()({
	component: () => (
		<React.Fragment>
			<ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
				<Outlet />
			</ThemeProvider>
			<TanStackRouterDevtools />
		</React.Fragment>
	),
})
