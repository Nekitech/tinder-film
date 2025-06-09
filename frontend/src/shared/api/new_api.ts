import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";
import {paths} from "./generated/schema";

const fetchClient = createFetchClient<paths>({
	baseUrl: import.meta.env.VITE_API_URL,
});

export const $api = createClient(fetchClient);