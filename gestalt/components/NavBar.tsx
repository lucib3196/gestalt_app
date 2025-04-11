"use client";

import Link from "next/link";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";

type LinkInfo = {
  name: string;
  path: string;
};

type NavBarProps = {
  app_name: string;
  links: LinkInfo[]; // optional if you want to pass dynamic links
};

const NavBar = ({ app_name, links }: NavBarProps) => {
  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
      <Container fluid>
        <Navbar.Brand as={Link} href="/">
          {app_name}
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          <Nav className="me-auto">
            {/* Static Home Link */}
            <Nav.Link as={Link} href="/">Home</Nav.Link>

            {/* About Dropdown */}
            <NavDropdown title="About" id="about-dropdown">
              <NavDropdown.Item as={Link} href="/#generators-section">Get Started</NavDropdown.Item>
              <NavDropdown.Item as={Link} href="/#key-features">Key Features</NavDropdown.Item>
            </NavDropdown>

            {/* Generate Dropdown */}
            <NavDropdown title="Generate" id="generate-dropdown">
              <NavDropdown.Item as={Link} href="/generators/text_generator">QuickQuery</NavDropdown.Item>
              <NavDropdown.Item as={Link} href="/generators/image_generator">VisualExtract</NavDropdown.Item>
            </NavDropdown>

            {/* Dynamic Links if needed */}
            {links?.map((link, idx) => (
              <Nav.Link as={Link} href={link.path} key={idx}>
                {link.name}
              </Nav.Link>
            ))}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavBar;
