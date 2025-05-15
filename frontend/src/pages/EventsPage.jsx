import { useEffect, useState } from 'react';
import { Container, Spinner, Alert, Table } from 'react-bootstrap';

export default function EventsPage() {
  const [data, setData] = useState({ pending_events: [], executed_events: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/events/`)
      .then(res => {
        if (!res.ok) throw new Error(`Status ${res.status}`);
        return res.json();
      })
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const renderTable = (events, title) => (
    <>
      <h2 className="mt-4">{title}</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Book Title</th>
            <th>Qty</th>
            <th>Scheduled</th>
            <th>Executed At</th>
          </tr>
        </thead>
        <tbody>
          {events.map(ev => (
            <tr key={ev.id}>
              <td>{ev.id}</td>
              <td>{ev.book_title}</td>
              <td>{ev.quantity}</td>
              <td>{new Date(ev.scheduled_for).toLocaleString()}</td>
              <td>{ev.executed ? new Date(ev.executed_at).toLocaleString() : '-'}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </>
  );

  if (loading) return <Container><Spinner animation="border" /></Container>;
  if (error) return <Container><Alert variant="danger">{error}</Alert></Container>;

  return (
    <Container>
      <h1>Restock Events</h1>
      {renderTable(data.pending_events, 'Pending Events')}
      {renderTable(data.executed_events, 'Executed Events')}
    </Container>
  );
}