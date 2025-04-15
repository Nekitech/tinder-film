import {createContext, ReactNode, useContext, useState} from 'react';
import {Film} from "@/shared/types/films.type.ts";

const useFilmState = (initialFilms: Film[]) => useState<Film[]>(initialFilms);
export const FilmsContext = createContext<ReturnType<typeof useFilmState> | null>(null);

export const FilmsProvider = (
	{ initialFilms,
		children }:
    { initialFilms: Film[],
        children: ReactNode }) => {
	const [films, setFilms] = useFilmState(initialFilms)
	return (
		<FilmsContext.Provider value={[films, setFilms]}>
			{children}
		</FilmsContext.Provider>
	);
};

export default FilmsProvider;

export const useFilmsContext = () => {
	const films = useContext(FilmsContext);
	if (!films) {
		throw new Error("useFilmContext must be used within a FilmProvider");
	}
	return films;
};