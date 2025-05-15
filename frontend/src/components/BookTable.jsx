import { Table } from 'react-bootstrap';
import { Link } from 'react-router-dom';

export default function BookTable({ books }) {
  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Author</th>
          <th>Price</th>
          <th>Stock</th>
        </tr>
      </thead>
      <tbody>
        {books.map(b => (
          <tr key={b.id}>
            <td>{b.id}</td>
            <td>
              <Link to={`/books/${b.id}`}>{b.title}</Link>
            </td>
            <td>{b.author}</td>
            <td>${Number(b.price).toFixed(2)}</td>
            <td>{b.stock}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}