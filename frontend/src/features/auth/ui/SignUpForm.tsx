import {useForm} from "react-hook-form";
import {z} from "zod";
import {zodResolver} from "@hookform/resolvers/zod";
import {Form, FormControl, FormField, FormItem, FormLabel, FormMessage} from "@/shared/components/ui/form";
import {Button} from "@/shared/components/ui/button";
import {Input} from "@/shared/components/ui/input";
import {useAuth} from "@/shared/providers/auth.provider.tsx";
import {Link, useNavigate} from "@tanstack/react-router";

const signUpFormSchema = z.object({
	username: z.string()
		.min(2, {message: "Username must be at least 2 characters long"})
		.max(100, {message: "Username must not exceed 100 characters"}),
	password: z.string()
		.min(3, {message: "Password must be at least 3 characters long"})
		.max(32, {message: "Password must not exceed 32 characters"})
});

const SignUpForm = () => {
	const {sign_up} = useAuth();
	const navigate = useNavigate()


	const form = useForm<z.infer<typeof signUpFormSchema>>({
		resolver: zodResolver(signUpFormSchema),
		defaultValues: {
			username: "",
			password: ""
		}
	});

	async function onSubmit(values: z.infer<typeof signUpFormSchema>) {
		try {
			await sign_up!(values.username, values.password);

			navigate({
				to: "/login"
			});
			console.log("Signup successful!");

		} catch (error) {
			console.error("Signup failed:", error);
		}
	}

	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 border-2 border-grey-500 rounded-2xl p-4">
				<FormLabel>Sign Up</FormLabel>
				<FormField
					control={form.control}
					name="username"
					render={({field}) => (
						<FormItem>
							<FormLabel>Username</FormLabel>
							<FormControl>
								<Input type="text" placeholder="Enter your username" {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="password"
					render={({field}) => (
						<FormItem>
							<FormLabel>Password</FormLabel>
							<FormControl>
								<Input type="password" placeholder="Enter your password" {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<div className={'w-full flex justify-around items-center'}>
					<Link
						to="/login"
						className={'underline'}
					>
						Sign in
					</Link>
					<Button type="submit" className="cursor-pointer">Sign Up</Button>
				</div>
			</form>
		</Form>
	);
};

export default SignUpForm;