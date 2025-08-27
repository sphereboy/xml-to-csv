import { useState } from "react";
import Head from "next/head";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [platform, setPlatform] = useState("wordpress");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const platforms = [
    { value: "wordpress", label: "WordPress" },
    { value: "ghost", label: "Ghost" },
    { value: "jekyll", label: "Jekyll" },
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

      // This will be your Python backend URL
      const response = await fetch(
        "https://xml-to-csv.onrender.com/api/convert",
        {
          method: "POST",
          body: formData,
        }
      );

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
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Head>
        <title>Framer Blog XML to CSV Converter</title>
        <meta
          name="description"
          content="Convert your blog XML exports to CSV format"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Framer Blog XML to CSV Converter
          </h1>
          <p className="text-lg text-gray-600">
            Convert your blog XML exports to CSV format for various platforms
          </p>
        </div>

        <div className="bg-white shadow-lg rounded-lg p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="file"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                XML File
              </label>
              <input
                type="file"
                id="file"
                accept=".xml"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                required
              />
              <p className="mt-1 text-sm text-gray-500">
                Select an XML file exported from your blog platform
              </p>
            </div>

            <div>
              <label
                htmlFor="platform"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Target Platform
              </label>
              <select
                id="platform"
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
            </div>

            <button
              type="submit"
              disabled={loading || !file}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Converting..." : "Convert to CSV"}
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
              <p className="text-sm text-green-600">
                Your XML file has been successfully converted to CSV format.
              </p>
              {result.download_url && (
                <a
                  href={result.download_url}
                  download
                  className="mt-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                >
                  Download CSV
                </a>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
