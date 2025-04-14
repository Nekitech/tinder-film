import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import FilmsProvider from "@/shared/store/films.store.tsx";
import {getFilms} from "@/shared/api/films.api.ts";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <FilmsProvider initialFilms={getFilms()} >
          <App />
      </FilmsProvider>
  </StrictMode>,
)
