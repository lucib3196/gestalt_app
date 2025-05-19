export const loadingComponent: React.ReactNode = (
  <div className="text-center p-4">
    <div className="spinner-border text-primary" role="status">
      <span className="visually-hidden">Loading...</span>
    </div>
  </div>
);

export const errorComponent: React.ReactNode = (
  <div className="alert alert-danger">Error loading modules</div>
);
