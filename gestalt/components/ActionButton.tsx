type ActionButtonProps = {
  onClick: () => Promise<any>;
  label?: string;
  className?: string;
  disabled?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
};

const ActionButton: React.FC<ActionButtonProps> = ({
  onClick,
  label = "Save",
  className = "",
  disabled = false,
  loading = false,
  icon,
}) => {
  const handleClick = async () => {
    if (disabled || loading) return;
    try {
      await onClick();
    } catch (error) {
      console.error("Action Error:", error);
    }
  };

  return (
    <button
      disabled={disabled || loading}
      className={`inline-flex items-center justify-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-xl shadow-sm transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 active:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
      onClick={handleClick}
    >
      {loading ? (
        <svg
          className="animate-spin mr-2 h-4 w-4 text-white"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v8H4z"
          ></path>
        </svg>
      ) : (
        icon && <span className="mr-2">{icon}</span>
      )}
      {label}
    </button>
  );
};

export default ActionButton;
