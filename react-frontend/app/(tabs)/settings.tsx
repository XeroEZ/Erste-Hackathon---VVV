import {
  View,
  Text,
  Image,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import React, { useState, useEffect } from "react";
import { images } from "@/constants/images";
import { router } from "expo-router";

import brightnessIcon from "@/assets/icons/brightness.png";
import languageIcon from "@/assets/icons/language.png";
import lockOpenIcon from "@/assets/icons/lock_open.png";
import supportIcon from "@/assets/icons/support.png";
import userIcon from "@/assets/icons/user.png";
import logoutIcon from "@/assets/icons/logout.png";

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

const Settings = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await fetch(
        `${process.env.EXPO_PUBLIC_API_URL}api/core/user/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch user data");
      }

      const data = await response.json();
      setUser(data);
    } catch (err) {
      console.error("Error fetching user:", err);
      Alert.alert("Chyba", "Nepodarilo sa načítať používateľa");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      const response = await fetch(
        `${process.env.EXPO_PUBLIC_API_URL}api/core/logout/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        }
      );

 
      router.replace("/(auth)/signin");

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.log("Logout completed with warning:", errorData);
      }
    } catch (err) {
      console.log("Logout completed:", err);
      router.replace("/(auth)/signin");
    }
  };

  const confirmLogout = () => {
    Alert.alert(
      "Odhlásiť sa",
      "Naozaj sa chcete odhlásiť?",
      [
        {
          text: "Zrušiť",
          style: "cancel",
        },
        {
          text: "Odhlásiť",
          style: "destructive",
          onPress: handleLogout,
        },
      ],
      { cancelable: true }
    );
  };

  if (loading) {
    return (
      <View className="flex-1 bg-black items-center justify-center">
        <ActivityIndicator size="large" color="#FFFFFF" />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      <ScrollView
        contentContainerStyle={{
          paddingHorizontal: 22,
          paddingTop: 40,
          paddingBottom: 50,
        }}
        className="flex-1"
      >
        {/* Title */}
        <View className="mb-6">
          <Text className="text-white text-2xl font-semibold">Nastavenia</Text>
        </View>

        {/* Profile card */}
        <View
          className="bg-box rounded-3xl p-5 mb-8 border border-stroke"
          style={{ borderWidth: 0.5 }}
        >
          <View className="flex-row items-center">
            <View className="w-16 h-16 rounded-full bg-white/15 items-center justify-center mr-4">
              <Image
                source={userIcon}
                className="w-8 h-8"
                resizeMode="contain"
              />
            </View>
            <View className="flex-1">
              <Text className="text-white text-xl font-semibold">
                {user ? `${user.first_name} ${user.last_name}` : "Používateľ"}
              </Text>
            </View>
          </View>

          <View className="h-px bg-white/15 my-5" />
          {/* Detail lines */}
          <View className="space-y-4">
            <DetailLine label="User ID:" value={user?.username || "N/A"} />
            <DetailLine label="Email:" value={user?.email || "N/A"} />
          </View>
        </View>

        {/* Setting rows with margin spacing */}
        <View>
          <SettingRow icon={brightnessIcon} title="Motív" subtitle="tmavý" />
          <SettingRow icon={languageIcon} title="Jazyk" subtitle="slovenčina" />
          <SettingRow
            icon={lockOpenIcon}
            title="Povolenia"
            subtitle="v poriadku"
          />
          <SettingRow
            icon={supportIcon}
            title="Podpora"
            subtitle="kontaktujte nás"
            last
          />
        </View>

        {/* Sign out */}
        <TouchableOpacity
          activeOpacity={0.7}
          className="mt-8 rounded-3xl bg-white/12 overflow-hidden"
          onPress={confirmLogout}
        >
          <View className="py-4 flex-row items-center justify-center">
            <Image
              source={logoutIcon}
              className="w-5 h-5 mr-2"
              resizeMode="contain"
              style={{ tintColor: "#ef4444" }}
            />
            <Text className="text-red-500 font-semibold text-lg">
              Odhlásiť sa
            </Text>
          </View>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
};

const DetailLine = ({
  label,
  value,
}: {
  label: string;
  value: string;
}) => (
  <View className="flex-row items-center mb-3">
    <Text className="text-white/40 w-24">{label}</Text>
    <Text className="text-white flex-1">{value}</Text>
  </View>
);

type RowProps = { icon: any; title: string; subtitle?: string; last?: boolean };
const SettingRow = ({ icon, title, subtitle, last }: RowProps) => (
  <TouchableOpacity
    activeOpacity={0.6}
    className={`flex-row items-center rounded-2xl bg-box px-5 py-4 mb-6 border border-stroke ${
      last ? "mb-0" : ""
    }`}
    style={{ borderWidth: 0.5 }}
  >
    <View className="w-9 h-9 rounded-full bg-white/15 items-center justify-center mr-4 overflow-hidden">
      <Image source={icon} className="w-6 h-6" resizeMode="contain" />
    </View>
    <View className="flex-1">
      <Text className="text-white text-base font-medium">{title}</Text>
      {subtitle ? (
        <Text className="text-white/50 text-xs mt-0.5">{subtitle}</Text>
      ) : null}
    </View>
  </TouchableOpacity>
);

export default Settings;