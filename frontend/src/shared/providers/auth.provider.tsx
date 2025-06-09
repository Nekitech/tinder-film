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
    sign_up?: (username: string, password: string) => Promise<void>;
    logout?: () => void;
    isAuthenticated: (() => boolean) | undefined;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	const accessToken = localStorage.getItem('access_token');

	const [user, setUser] = useState<AuthUser | null>(null);

	const {mutateAsync, status: statusLogin} = $api.useMutation(
		"post",
		"/login",
	);

	const {mutateAsync: signUpMutate} = $api.useMutation(
		"post",
		"/register",
	);

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

		if (userInfo) {
			setUser({
				...userInfo
			});
		}

		return {
			userData: userInfo,
			statusLogin
		}
	};

	const sign_up = async (username: string, password: string) => {
		try {
			await signUpMutate({
				params: {
					query: {
						username,
						password
					}
				}
			});

		} catch (error) {
			console.error("Signup error:", error);
			throw error;
		}
	}

	const logout = () => {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		setUser(null);
	};

	const isAuthenticated = () => {
		return localStorage.getItem('refresh_token') !== null;
	}

	return (
		<AuthContext.Provider value={{user, isAuthenticated, login, sign_up, logout}}>
			{ children }
		</AuthContext.Provider>
	);
};

export const useAuth = (): AuthContextType => {
	const context = useContext(AuthContext);
	if (!context) throw new Error('useAuth must be used within an AuthProvider');
	return context;
};