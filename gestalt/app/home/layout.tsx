
export const metadata = {
    title: 'Home Section',
    description: 'Page under /home route',
  };
  
  export default function HomeLayout({ children }: { children: React.ReactNode }) {
    return (
      <div>
        <h2>Home Layout</h2>
        {children}
      </div>
    );
  }
  