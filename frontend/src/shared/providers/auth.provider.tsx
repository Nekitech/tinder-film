import React, {createContext, useContext, useEffect, useState} from 'react';
import {$api} from "@/shared/api/new_api.ts";

type AuthUser = {
    sub: string;
    username: string;
    iat: number;
    exp: number;
    type: string
};

export type AuthContextType = {
    user: AuthUser | null;
    login?: (username: string, password: string) => Promise<{ userData: any, isPending: any, status: any }>;
    logout?: () => void;
    isAuthenticated: (() => boolean) | undefined;
};


const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	const accessToken = localStorage.getItem('access_token');
	// const refreshToken = localStorage.getItem('refresh_token');

	const [user, setUser] = useState<AuthUser | null>(null);
	const {mutateAsync, isPending, status} = $api.useMutation(
		"post",
		"/login",
	)

	// const refreshMutation = $auth_api.refresh.hook({
	// 	request: {
	// 		headers: {
	// 			Authorization: `Bearer ${refreshToken}`,
	// 		},
	// 	},
	// }, queryClient);

	const {data, isSuccess, refetch} = $api.useQuery(
		"get",
		"/users/me/",
		{
			headers: {
				"Authorization": `Bearer ${accessToken}`,
			}
		}
	);

	useEffect(() => {
		if (isSuccess && data) {
			setUser({...data});
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
		const response = await mutateAsync({
			body: {
				username,
				password
			}
		});

		localStorage.setItem('access_token', response.access_token);
		localStorage.setItem('refresh_token', response.refresh_token!);

		const {data: userInfo} = await refetch();

		console.log(userInfo)

		if (userInfo) {
			setUser({
				...userInfo
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
