import Axios, {AxiosError, AxiosRequestConfig} from 'axios';

export const AXIOS_INSTANCE = Axios.create(
	{
		baseURL: 'http://127.0.0.1:8000',
		withCredentials: true
	});

// add a second `options` argument here if you want to pass extra options to each generated query
export const customInstance = <T>(
	config: AxiosRequestConfig,
	options?: AxiosRequestConfig,
): Promise<T> => {
	const promise = AXIOS_INSTANCE({
		...config,
		...options,
	}).then(({data}) => data);

	return promise;
};

export type ErrorType<Error> = AxiosError<Error>;

export type BodyType<BodyData> = BodyData;
