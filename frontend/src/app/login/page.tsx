import LoginTabs from "@/components/login/login-tabs";
import { title } from "@/styles/primitives";

export default function LoginPage() {
  return (
    <main className="mx-auto h-[calc(100vh_-_64px)] w-full max-w-7xl px-6">
      <div className="flex h-full w-full flex-col items-center space-y-6 rounded-lg p-6">
        <div className="flex w-full flex-col items-center justify-center gap-10">
          <h1
            className={title({
              size: "sm",
            })}
          >
            Sign in to Easolve
          </h1>
        </div>
        <LoginTabs />
      </div>
    </main>
  );
}
