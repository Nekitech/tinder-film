import {StrictMode} from 'react'
import './index.css'
import ReactDOM from 'react-dom/client';
import {createRouter, RouterProvider} from "@tanstack/react-router";
import {routeTree} from "@/routeTree.gen.ts";
import {AuthProvider, useAuth} from "@/shared/providers/auth.provider.tsx";
import {QueryClient, QueryClientProvider} from '@tanstack/react-query';

const router = createRouter({
	routeTree,
	defaultPreload: 'intent',
	scrollRestoration: true,
	context: {
		auth: {
			isAuthenticated: false,
			user: null
		}
	}

})

// const loginRootRoute = createRootRoute({
//     component: LoginForm,
// })

// const loginRouter = createRoute({
//     getParentRoute: () => <></>,
//     path: "/login",
//     component: function Login (){
//         return <LoginForm/>
//     }
// })


declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router
    }
}
const queryClient = new QueryClient()

const rootElement = document.getElementById('root')!

function AuthApp() {
	const auth = useAuth()
	console.log(auth)
	return <RouterProvider router={router} context={{auth}} />
}

if (!rootElement?.innerHTML) {
	const root = ReactDOM.createRoot(rootElement)
	root.render(
		<StrictMode>
			<QueryClientProvider client={queryClient}>
				<AuthProvider>
					{ /*<FilmsProvider>*/ }
					<AuthApp />
					{ /*</FilmsProvider>*/ }
				</AuthProvider>
			</QueryClientProvider>
		</StrictMode>
	)
}