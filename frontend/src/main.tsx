import {StrictMode} from 'react'
import './index.css'
import FilmsProvider from "@/shared/store/films.store.tsx";
import {getFilms} from "@/shared/api/films.api.ts";
import ReactDOM from 'react-dom/client';
import {createRouter, RouterProvider} from "@tanstack/react-router";
import {routeTree} from "@/routeTree.gen.ts";

const router = createRouter({
	routeTree,
	defaultPreload: 'intent',
	scrollRestoration: true,

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

const rootElement = document.getElementById('root')!

if (!rootElement?.innerHTML) {
	const root = ReactDOM.createRoot(rootElement)
	root.render(
		<StrictMode>
			<FilmsProvider initialFilms={getFilms()} >
				<RouterProvider router={router} />
			</FilmsProvider>
		</StrictMode>

	)
}