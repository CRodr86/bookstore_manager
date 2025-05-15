import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Spinner, Alert, Form, Button } from 'react-bootstrap';

export default function BookFormPage() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();
  const [form, setForm] = useState({ title: '', author: '', description: '', price: '', stock: '' });
  const [loading, setLoading] = useState(isEdit);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEdit) {
      fetch(`${import.meta.env.VITE_API_URL}/books/${id}/`)
        .then(res => res.json())
        .then(({ title, author, description, price, stock }) => {
          setForm({ title, author, description, price, stock });
          setLoading(false);
        });
    }
  }, [id, isEdit]);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    const method = isEdit ? 'PUT' : 'POST';
    const url = isEdit
      ? `${import.meta.env.VITE_API_URL}/books/${id}/`
      : `${import.meta.env.VITE_API_URL}/books/`;

    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
      .then(res => res.json())
      .then(() => {
        navigate(isEdit ? `/books/${id}` : '/');
      })
      .catch(err => setError(err.message));
  };

  if (loading) return <Container><Spinner animation="border" /></Container>;

  return (
    <Container>
      <h1>{isEdit ? 'Edit Book' : 'Add New Book'}</h1>
      {error && <Alert variant="danger">{error}</Alert>}
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Title</Form.Label>
          <Form.Control name="title" value={form.title} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Author</Form.Label>
          <Form.Control name="author" value={form.author} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Description</Form.Label>
          <Form.Control as="textarea" rows={3} name="description" value={form.description} onChange={handleChange} />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Price</Form.Label>
          <Form.Control type="number" step="0.01" name="price" value={form.price} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Stock</Form.Label>
          <Form.Control type="number" name="stock" value={form.stock} onChange={handleChange} required />
        </Form.Group>
        <Button type="submit">{isEdit ? 'Update' : 'Create'}</Button>
      </Form>
    </Container>
  );
}