import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Container, Spinner, Alert, Button, Form } from 'react-bootstrap';

export default function BookDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [book, setBook] = useState(null);
  const [qty, setQty] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/books/${id}/`)
      .then(res => {
        if (!res.ok) throw new Error(`Status ${res.status}`);
        return res.json();
      })
      .then(data => {
        setBook(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  const handleBuy = e => {
    e.preventDefault();
    setMessage('');
    fetch(`${import.meta.env.VITE_API_URL}/book/buy/${id}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quantity: qty }),
    })
      .then(res => res.ok ? res.json() : res.json().then(data => { throw new Error(data.detail); }))
      .then(() => setMessage('Purchase successful!'))
      .catch(err => setMessage(`Error: ${err.message}`));
  };

  const handleDelete = () => {
    fetch(`${import.meta.env.VITE_API_URL}/books/${id}/`, { method: 'DELETE' })
      .then(res => {
        if (res.ok) navigate('/');
        else throw new Error('Delete failed');
      })
      .catch(err => setMessage(`Error: ${err.message}`));
  };

  if (loading) return <Container><Spinner animation="border" /></Container>;
  if (error) return <Container><Alert variant="danger">{error}</Alert></Container>;

  return (
    <Container>
      <h1>{book.title}</h1>
      <p><strong>Author:</strong> {book.author}</p>
      <p><strong>Description:</strong> {book.description}</p>
      <p><strong>Price:</strong> ${Number(book.price).toFixed(2)}</p>
      <p><strong>Stock:</strong> {book.stock}</p>

      <div className="mb-3">
        <Link to={`/books/${id}/edit`}><Button variant="secondary">Edit</Button></Link>{' '}
        <Button variant="danger" onClick={handleDelete}>Delete</Button>
      </div>

      <h2>Buy More Stock</h2>
      <Form onSubmit={handleBuy} className="d-flex align-items-center mb-3">
        <Form.Label className="me-2 mb-0">Quantity:</Form.Label>
        <Form.Control
          type="number"
          min="1"
          value={qty}
          onChange={e => setQty(Number(e.target.value))}
          style={{ width: '100px', marginRight: '1rem' }}
        />
        <Button type="submit">Buy</Button>
      </Form>

      {message && (
        <Alert variant={message.startsWith('Error') ? 'danger' : 'success'}>
          {message}
        </Alert>
      )}

      <Link to="/">← Back to list</Link>
    </Container>
  );
}