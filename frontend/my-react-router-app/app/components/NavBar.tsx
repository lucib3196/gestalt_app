import { Link } from "react-router-dom";
import { Navbar, Nav, Container, NavDropdown, Form, FormControl, Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

type LinkInfo = {
  name: string;
  ref_link: string;
};

type NavBarProps = {
  app_name: string;
  links: LinkInfo[];
};

const NavBar = ({ app_name, links }: NavBarProps) => {
  function handleLinks() {
    return links.map((link, idx) => (
      <Nav.Link as={Link} to={link.ref_link} key={idx}>
        {link.name}
      </Nav.Link>
    ));
  }

  return (
    <Navbar bg="light" expand="lg">
      <Container fluid>
        <Navbar.Brand as={Link} to="/">
          {app_name}
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          <Nav className="me-auto">
            {/* This section is valid links */}
            {handleLinks()}
            {/* This section does not really work for now but keep it */}
            <NavDropdown title="Dropdown" id="basic-nav-dropdown">
              <NavDropdown.Item as={Link} to="/action">
                Action
              </NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/another-action">
                Another action
              </NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item as={Link} to="/something-else">
                Something else here
              </NavDropdown.Item>
            </NavDropdown>
            <Nav.Link disabled>Disabled</Nav.Link>
          </Nav>
          <Form className="d-flex">
            <FormControl
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
            />
            <Button variant="outline-success">Search</Button>
          </Form>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavBar;
