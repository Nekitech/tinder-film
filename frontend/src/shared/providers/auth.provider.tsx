import React, {createContext, useContext, useEffect, useState} from 'react';
import {useQueryClient} from '@tanstack/react-query';
import {$auth_api} from "@/shared/api/auth.api.ts";

type AuthUser = {
    userId: string;
    username: string;
};

export type AuthContextType = {
    user: AuthUser | null;
    login?: (username: string, password: string) => Promise<{ userData: any, isPending: any, status: any }>;
    logout?: () => void;
    isAuthenticated: () => boolean
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	const queryClient = useQueryClient();
	const accessToken = localStorage.getItem('access_token');
	// const refreshToken = localStorage.getItem('refresh_token');

	const [user, setUser] = useState<AuthUser | null>(null);
	const {mutateAsync, isPending, status} = $auth_api.login.hook();

	// const refreshMutation = $auth_api.refresh.hook({
	// 	request: {
	// 		headers: {
	// 			Authorization: `Bearer ${refreshToken}`,
	// 		},
	// 	},
	// }, queryClient);

	const {data, isSuccess, refetch} = $auth_api.usersMe.hook(
		accessToken
			? {
				request: {
					headers: {
						Authorization: `Bearer ${accessToken}`,
					},
				},
			}
			: undefined,
		queryClient
	);

	useEffect(() => {
		if (isSuccess && data) {
			setUser({userId: data.sub, username: data.username});
		}
	}, [isSuccess, data]);

	// useEffect(() => {
	// 	async function tryRefresh() {
	// 		if (!accessToken) {
	// 			logout();
	// 			return;
	// 		}
	//
	// 		if (!isSuccess) {
	// 			if (refreshToken) {
	// 				try {
	// 					const refreshed = await refreshMutation.mutateAsync();
	// 					localStorage.setItem('access_token', refreshed.access_token);
	//
	// 					await queryClient.invalidateQueries();
	// 					await refetch();
	// 				} catch {
	// 					logout();
	// 				}
	// 			} else {
	// 				logout();
	// 			}
	// 		}
	// 	}
	//
	// 	tryRefresh();
	// }, [isSuccess, accessToken, refreshToken, refreshMutation, queryClient, refetch]);

	const login = async (username: string, password: string) => {
		const response = await mutateAsync({data: {username, password}});

		localStorage.setItem('access_token', response.access_token);
		localStorage.setItem('refresh_token', response.refresh_token!);

		const {data: userInfo} = await refetch();

		console.log(userInfo)

		if (userInfo) {
			setUser({
				userId: userInfo.sub,
				username: userInfo.username,
			});
		}

		return {
			userData: userInfo,
			isPending,
			status
		}
	};


	const logout = () => {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		setUser(null);
		queryClient.clear();
	};

	const isAuthenticated = () => {
		return localStorage.getItem('refresh_token') !== null;
	}

	return (
		<AuthContext.Provider value={{user, isAuthenticated, login, logout}}>
			{ children }
		</AuthContext.Provider>
	);
};

export const useAuth = (): AuthContextType => {
	const context = useContext(AuthContext);
	if (!context) throw new Error('useAuth must be used within an AuthProvider');
	return context;
};
