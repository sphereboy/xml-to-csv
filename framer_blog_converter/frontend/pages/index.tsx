import { useState } from "react";
import Head from "next/head";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [platform, setPlatform] = useState("wordpress");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Use production API URL
  const API_BASE_URL =
    process.env.NODE_ENV === "production"
      ? "https://xml-to-csv.onrender.com"
      : "http://localhost:5001";

  const platforms = [
    {
      value: "wordpress",
      label: "WordPress (Squarespace Export)",
      description: "Primary format for Squarespace exports",
    },
    {
      value: "ghost",
      label: "Ghost",
      description: "Alternative blog platform",
    },
    { value: "jekyll", label: "Jekyll", description: "Static site generator" },
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("platform", platform);

      // Use the correct API URL for production/development
      const response = await fetch(`${API_BASE_URL}/api/convert`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <Head>
        <title>Squarespace to Framer CSV Converter</title>
        <meta
          name="description"
          content="Convert Squarespace XML exports to Framer-ready CSV format. Specialized for easy Squarespace to Framer website migration."
        />
      </Head>

      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Squarespace to Framer CSV Converter
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            Convert your Squarespace XML exports to Framer-ready CSV format for
            seamless website migration
          </p>
          <p className="text-sm text-gray-500">
            Specialized for Squarespace exports • Optimized for Framer import •
            Also supports WordPress, Ghost, and Jekyll
          </p>
        </div>

        <div className="bg-white shadow-lg rounded-lg p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Squarespace XML Export File
              </label>
              <input
                type="file"
                accept=".xml"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                required
              />
              <p className="mt-1 text-sm text-gray-500">
                Upload your Squarespace XML export file (typically exported as
                WordPress format)
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Export Format
              </label>
              <select
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                {platforms.map((p) => (
                  <option key={p.value} value={p.value}>
                    {p.label}
                  </option>
                ))}
              </select>
              <p className="mt-1 text-sm text-gray-500">
                {platforms.find((p) => p.value === platform)?.description}
              </p>
            </div>

            <button
              type="submit"
              disabled={loading || !file}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Converting..." : "Convert to Framer CSV"}
            </button>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          {result && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
              <h3 className="text-lg font-medium text-green-800 mb-2">
                Conversion Complete!
              </h3>
              <p className="text-sm text-green-600 mb-3">
                Your Squarespace XML has been converted to Framer-ready CSV
                format.
              </p>
              <p className="text-xs text-green-600 mb-3">
                💡 <strong>Next step:</strong> Import this CSV into your Framer
                project using the CMS or Data components.
              </p>
              {result.download_url && (
                <a
                  href={result.download_url}
                  download
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                >
                  Download Framer CSV
                </a>
              )}
            </div>
          )}
        </div>

        {/* Squarespace to Framer Workflow */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-blue-900 mb-4">
            🚀 Squarespace to Framer Migration Workflow
          </h3>
          <div className="space-y-3 text-sm text-blue-800">
            <div className="flex items-start space-x-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium">
                1
              </span>
              <span>
                Export your Squarespace blog as XML (WordPress format)
              </span>
            </div>
            <div className="flex items-start space-x-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium">
                2
              </span>
              <span>Upload the XML file here and convert to CSV</span>
            </div>
            <div className="flex items-start space-x-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium">
                3
              </span>
              <span>Import the CSV into your Framer project's CMS</span>
            </div>
            <div className="flex items-start space-x-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium">
                4
              </span>
              <span>
                Build your new Framer website with your existing content!
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
