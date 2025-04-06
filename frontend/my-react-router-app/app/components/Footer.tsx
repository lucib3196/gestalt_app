import {
  Container,
  Row,
  Col,
  Stack,
  Image,
  Nav,
  NavLink,
} from "react-bootstrap";
import "~/styles/Footer.css";

// Need to add more information on this
export default function Footer() {
  return (
    <footer className="my-footer border-top py-4 mt-auto">
      <Container fluid className="text-center">
        <Row>
          <p>
            &copy; 2024 University of California, Riverside. All rights
            reserved.
          </p>
        </Row>
      </Container>
    </footer>
  );
}
