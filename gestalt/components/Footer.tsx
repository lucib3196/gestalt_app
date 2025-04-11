import {
  Container,
  Row,
  Col,
  Stack,
  Image,
  Nav,
  NavLink,
} from "react-bootstrap";
import "../styles/Footer.css";
import Link from "next/link";


// Need to add more information on this
export default function Footer() {
  return (
    <footer className="my-footer">
      <Container fluid className="text-center">
        <Row>
          <p>
            &copy; 2024 University of California, Riverside. All rights
            reserved.
          </p>
        </Row>
        <Row>
          <p>
            <Link href="/license" className="footer-link" target="_blank">
              License
            </Link>
          </p>
        </Row>
      </Container>
    </footer>
  );
}
