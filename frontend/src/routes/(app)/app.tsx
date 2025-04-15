import {createFileRoute, Outlet} from '@tanstack/react-router'
import {AppSidebar} from "@/shared/layouts/sidebar.tsx";
import {SidebarProvider, SidebarTrigger} from "@/shared/components/ui/sidebar.tsx";

export const Route = createFileRoute('/(app)/app')({
	component: RouteComponent,
})

function RouteComponent() {
	return (
		<SidebarProvider>
			<AppSidebar />
			<SidebarTrigger />
			<div className={'w-full'}>
				<Outlet />
			</div>
		</SidebarProvider>

	)
}
