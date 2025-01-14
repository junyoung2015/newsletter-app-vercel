"use client";

import { Button, Card, CardBody, CardHeader, Divider } from "@nextui-org/react";
import { logout } from "@/app/profile/actions";
import { LogoutIcon, SettingsIcon } from "@/icons";
import { subtitle, title } from "@/styles/primitives";

interface ProfileInfoProps {
  newsArr: MyNewsDto[];
}

export interface MyNewsDto {
  id: string;
  name: string;
  description: string;
  send_frequency: string;
}

const ProfileInfo: React.FC<ProfileInfoProps> = ({ newsArr }) => {
  return (
    <>
      <div className="flex w-full items-center justify-between">
        <h1
          className={title({
            size: "md",
          })}
        >
          Profile
        </h1>
        <Button
          aria-label="Logout"
          endContent={<LogoutIcon />}
          onPress={logout}
        >
          Sign out
        </Button>
      </div>
      <h1 className={title({ size: "sm", fullWidth: true })}>My News</h1>
      <div className="flex w-full flex-nowrap gap-6 overflow-x-auto p-6">
        {newsArr
          ? newsArr.map((news) => (
              <Card
                key={news.id ? news.id : news.name + `${Math.random()}`}
                classNames={{
                  base: "w-[300px] shrink-0",
                }}
              >
                <CardHeader className="flex justify-between">
                  <div className="flex flex-col items-start justify-center">
                    <h2 className={subtitle()}>{news.name}</h2>
                    <p>{news.send_frequency}</p>
                  </div>
                  <Button isIconOnly>
                    <SettingsIcon />
                  </Button>
                </CardHeader>
                <Divider />
                <CardBody>{news.description}</CardBody>
              </Card>
            ))
          : "No news found"}
      </div>
    </>
  );
};

export default ProfileInfo;
