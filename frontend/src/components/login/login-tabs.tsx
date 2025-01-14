"use client";

import { Button, Card, CardBody, Input, Tab, Tabs } from "@nextui-org/react";
import { useRouter } from "next/navigation";
import { useState } from "react";

interface LoginTabsProps {}

const LoginTabs: React.FC<LoginTabsProps> = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const router = useRouter();

  const handleSignIn = async () => {
    if (!email || !password) {
      console.error("Email and password are required.");
      alert("Email and password are required.");
      return;
    }

    const url = new URL("/api/user/login", "http://localhost:8000");
    let loginData = new URLSearchParams();
    loginData.append("username", email);
    loginData.append("password", password);

    try {
      const response: Response = await fetch(url.toString(), {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: loginData,
        credentials: "include",
      });
      if (!response.ok) {
        // TODO: handle error
        // e.g., 401 if invalid token
        console.error("Error signing in:", response.statusText);
        alert("Error signing in.");
        return;
      }
      router.push("/");
      router.refresh(); // NOTE: NOTE: /src/app/layout.tsx 에서 이메일을 보여주기 위해 (fetchUserEmail 을 다시 호출하기 위해) refresh 를 사용
    } catch (error) {
      console.error("Error signing in:", error);
      alert("Error signing in.");
    }
  };

  const handleSignUp = async () => {
    if (!email || !password || !confirmPassword) {
      console.error("Email, password, and confirm password are required.");
      alert("Email, password, and confirm password are required.");
      return;
    }

    if (password !== confirmPassword) {
      console.error("Passwords do not match.");
      alert("Passwords do not match.");
      return;
    }

    const url = new URL("/api/user/register", "http://localhost:8000");
    try {
      const response: Response = await fetch(url.toString(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: email, password }),
      });
      if (!response.ok) {
        // TODO: handle error
        // e.g., 401 if invalid token
        return;
      }
    } catch (error) {
      console.error("Error signing up:", error);
      alert("Error signing up.");
    }
  };

  return (
    <Tabs aria-label="Options">
      <Tab key="sign-in" title="Sign In">
        <Card
          classNames={{
            base: "w-[300px]",
          }}
        >
          <CardBody className="gap-4">
            <Input
              label="Email"
              placeholder="Enter your email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              label="Password"
              placeholder="Enter your password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button color="primary" size="md" onPress={handleSignIn}>
              Sign In
            </Button>
          </CardBody>
        </Card>
      </Tab>
      <Tab key="sign-up" title="Sign Up">
        <Card
          classNames={{
            base: "w-[300px]",
          }}
        >
          <CardBody className="gap-4">
            <Input
              label="Email"
              placeholder="Enter your email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              label="Password"
              placeholder="Enter your password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Input
              label="Confirm Password"
              placeholder="Enter your password to confirm"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            <Button color="primary" size="md" onPress={handleSignUp}>
              Sign Up
            </Button>
          </CardBody>
        </Card>
      </Tab>
    </Tabs>
  );
};

export default LoginTabs;
