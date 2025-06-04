import {
	Sidebar,
	SidebarContent,
	SidebarGroup,
	SidebarGroupContent,
	SidebarGroupLabel,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
} from "@/shared/components/ui/sidebar"
import {AlignCenterHorizontalIcon, Home, LogIn} from "lucide-react"
import {useAuth} from "@/shared/providers/auth.provider.tsx";

const items = [
	{
		title: "Home",
		url: "/app",
		icon: Home,
	},
	{
		title: "Recommendations",
		url: "/app/recommendations",
		icon: AlignCenterHorizontalIcon
	},
	{
		title: "Login",
		url: "/login",
		icon: LogIn,
	},
]

const appTitle = "Tinder Film"

export function AppSidebar() {
	const {logout} = useAuth()

	return (
		<Sidebar>
			<SidebarContent>
				<SidebarGroup>
					<SidebarGroupLabel>{ appTitle }</SidebarGroupLabel>
					<SidebarGroupContent>
						<SidebarMenu>
							{ items.map((item) => (
								<SidebarMenuItem key={item.title}>
									<SidebarMenuButton asChild>
										{
											item.title === 'Login' ? (
												<a href={item.url} onClick={logout}>
													<item.icon />
													<span>{ item.title }</span>
												</a>
											) : (
												<a href={item.url}>
													<item.icon />
													<span>{ item.title }</span>
												</a>
											)
										}

									</SidebarMenuButton>
								</SidebarMenuItem>
							)) }
						</SidebarMenu>
					</SidebarGroupContent>
				</SidebarGroup>
			</SidebarContent>
		</Sidebar>
	)
}
