import { createBrowserRouter, Outlet } from "react-router";
import Welcome from "./pages/Welcome";
import HowWeHelp from "./pages/HowWeHelp";
import GitHubUsername from "./pages/GitHubUsername";
import Loading from "./pages/Loading";
import Results from "./pages/Results";
import Journey from "./pages/Journey";
import Community from "./pages/Community";
import MainLayout from "./components/MainLayout";

function Layout() {
  return (
    <MainLayout>
      <Outlet />
    </MainLayout>
  );
}

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "/",
        Component: Welcome,
      },
      {
        path: "/how-we-help",
        Component: HowWeHelp,
      },
      {
        path: "/github-username",
        Component: GitHubUsername,
      },
      {
        path: "/loading",
        Component: Loading,
      },
      {
        path: "/results",
        Component: Results,
      },
      {
        path: "/journey",
        Component: Journey,
      },
      {
        path: "/community",
        Component: Community,
      },
    ]
  }
]);