import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import NavBar from './components/NavBar';
import BooksListPage from './pages/BooksListPage';
import BookDetailPage from './pages/BookDetailPage';
import BookFormPage from './pages/BookFormPage';
import EventsPage from './pages/EventsPage';

export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route
          path="/"
          element={
            <BooksListPage />
          }
        />
        <Route
          path="/books/new"
          element={
            <BookFormPage />
          }
        />
        <Route
          path="/books/:id"
          element={
            <BookDetailPage />
          }
        />
        <Route
          path="/books/:id/edit"
          element={
            <BookFormPage />
          }
        />
        <Route
          path="/events"
          element={
            <EventsPage />
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}