import { View, Text, Image, TouchableOpacity, ScrollView, Modal, TextInput, ActivityIndicator, Alert, KeyboardAvoidingView, Platform } from "react-native";
import React, { useState } from "react";
import { images } from "@/constants/images";

import brightnessIcon from "@/assets/icons/brightness.png";
import languageIcon from "@/assets/icons/language.png";
import lockOpenIcon from "@/assets/icons/lock_open.png";
import supportIcon from "@/assets/icons/support.png";
import userIcon from "@/assets/icons/user.png";
import editIcon from "@/assets/icons/edit.png";
import logoutIcon from "@/assets/icons/logout.png";
import { changePassword } from "@/services/api";

const Settings = () => {
  const [pwdModal, setPwdModal] = useState(false);
  const [currentPwd, setCurrentPwd] = useState("");
  const [newPwd, setNewPwd] = useState("");
  const [confirmPwd, setConfirmPwd] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const openPwdModal = () => setPwdModal(true);
  const closePwdModal = () => {
    setPwdModal(false);
    setCurrentPwd("");
    setNewPwd("");
    setConfirmPwd("");
  };

  const onSubmitChangePwd = async () => {
    if (!currentPwd || !newPwd || !confirmPwd) {
      Alert.alert("Chyba", "Vyplňte všetky polia.");
      return;
    }
    if (newPwd.length < 8) {
      Alert.alert("Chyba", "Nové heslo musí mať aspoň 8 znakov.");
      return;
    }
    if (newPwd !== confirmPwd) {
      Alert.alert("Chyba", "Heslá sa nezhodujú.");
      return;
    }
    try {
      setSubmitting(true);
      await changePassword({ current_password: currentPwd, new_password: newPwd, new_password_confirm: confirmPwd });
      setSubmitting(false);
      Alert.alert("Hotovo", "Heslo bolo zmenené. Prihláste sa znova.");
      closePwdModal();
      // Tip: po úspechu môžeš odhlásiť používateľa a presmerovať na Sign in.
    } catch (e: any) {
      setSubmitting(false);
      const msg = typeof e?.message === "string" ? e.message : "Zmena hesla zlyhala.";
      Alert.alert("Chyba", msg);
    }
  };

  return (
    <View className="flex-1 bg-black">
      <Image source={images.bg} className="absolute w-full h-full z-0" resizeMode="cover" />

      <ScrollView
        contentContainerStyle={{ paddingHorizontal: 22, paddingTop: 40, paddingBottom: 50 }}
        className="flex-1"
      >
        {/* Title */}
        <View className="mb-6">
          <Text className="text-white text-2xl font-semibold">Nastavenia</Text>
        </View>

        {/* Profile card */}
        <View className="bg-white/10 rounded-3xl p-5 mb-8">
          <View className="flex-row items-center">
            <View className="w-16 h-16 rounded-full bg-white/15 items-center justify-center mr-4">
              <Image source={userIcon} className="w-8 h-8" resizeMode="contain" />
            </View>
            <View className="flex-1">
              <View className="flex-row items-center">
                <Text className="text-white text-xl font-semibold">Janko Hraško</Text>
                <TouchableOpacity className="ml-3 px-2 py-1">
                  <Image source={editIcon} className="w-5 h-5" resizeMode="contain" />
                </TouchableOpacity>
              </View>
            </View>
          </View>

          <View className="h-px bg-white/15 my-5" />

          {/* Detail lines */}
          <View className="space-y-4">
            <DetailLine label="User ID:" value="jankohrasko11" />
            <DetailLine
              label="Heslo:"
              value="************"
              edit
              onPressEdit={openPwdModal}
            />
          </View>
        </View>

        {/* Setting rows with margin spacing */}
        <View>
          <SettingRow icon={brightnessIcon} title="Motív" subtitle="tmavý" />
          <SettingRow icon={languageIcon} title="Jazyk" subtitle="slovenčina" />
          <SettingRow icon={lockOpenIcon} title="Povolenia" subtitle="v poriadku" />
          <SettingRow icon={supportIcon} title="Podpora" subtitle="kontaktujte nás" last />
        </View>

        {/* Sign out */}
        <TouchableOpacity
          activeOpacity={0.7}
          className="mt-8 rounded-3xl bg-white/12 overflow-hidden"
        >
          <View className="py-4 flex-row items-center justify-center">
            <Image
              source={logoutIcon}
              className="w-5 h-5 mr-2"
              resizeMode="contain"
              style={{ tintColor: "#ef4444" }}
            />
            <Text className="text-red-500 font-semibold text-lg">Odhlásiť sa</Text>
          </View>
        </TouchableOpacity>
      </ScrollView>

      {/* Change password modal */}
      <Modal visible={pwdModal} animationType="slide" transparent onRequestClose={closePwdModal}>
        <View className="flex-1 bg-black/60 items-center justify-end">
          <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} className="w-full">
            <View className="bg-neutral-900 rounded-t-3xl p-6">
              <Text className="text-white text-xl font-semibold mb-4">Zmeniť heslo</Text>

              <Text className="text-white/70 mb-2">Aktuálne heslo</Text>
              <TextInput
                value={currentPwd}
                onChangeText={setCurrentPwd}
                placeholder="••••••••"
                placeholderTextColor="#8b8b8b"
                secureTextEntry
                className="bg-white/10 rounded-xl px-4 py-3 text-white mb-4"
              />

              <Text className="text-white/70 mb-2">Nové heslo</Text>
              <TextInput
                value={newPwd}
                onChangeText={setNewPwd}
                placeholder="min. 8 znakov"
                placeholderTextColor="#8b8b8b"
                secureTextEntry
                className="bg-white/10 rounded-xl px-4 py-3 text-white mb-4"
              />

              <Text className="text-white/70 mb-2">Potvrdenie nového hesla</Text>
              <TextInput
                value={confirmPwd}
                onChangeText={setConfirmPwd}
                placeholder="zopakujte nové heslo"
                placeholderTextColor="#8b8b8b"
                secureTextEntry
                className="bg-white/10 rounded-xl px-4 py-3 text-white mb-6"
              />

              <View className="flex-row">
                <TouchableOpacity onPress={closePwdModal} disabled={submitting} className="flex-1 mr-3 bg-white/10 rounded-xl py-3 items-center">
                  <Text className="text-white">Zrušiť</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={onSubmitChangePwd} disabled={submitting} className="flex-1 bg-white/20 rounded-xl py-3 items-center">
                  {submitting ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-semibold">Uložiť</Text>}
                </TouchableOpacity>
              </View>
            </View>
          </KeyboardAvoidingView>
        </View>
      </Modal>
    </View>
  );
};

const DetailLine = ({
  label,
  value,
  edit,
  onPressEdit,
}: {
  label: string;
  value: string;
  edit?: boolean;
  onPressEdit?: () => void;
}) => (
  <View className="flex-row items-center">
    <Text className="text-white/40 w-24">{label}</Text>
    <Text className="text-white flex-1">{value}</Text>
    {edit ? (
      <TouchableOpacity onPress={onPressEdit} className="pl-2">
        <Image source={editIcon} className="w-4 h-4" resizeMode="contain" />
      </TouchableOpacity>
    ) : null}
  </View>
);

type RowProps = { icon: any; title: string; subtitle?: string; last?: boolean };
const SettingRow = ({ icon, title, subtitle, last }: RowProps) => (
  <TouchableOpacity
    activeOpacity={0.6}
    className={`flex-row items-center rounded-2xl bg-white/10 px-5 py-4 mb-6 ${last ? "mb-0" : ""}`}
  >
    <View className="w-9 h-9 rounded-full bg-white/15 items-center justify-center mr-4 overflow-hidden">
      <Image source={icon} className="w-6 h-6" resizeMode="contain" />
    </View>
    <View className="flex-1">
      <Text className="text-white text-base font-medium">{title}</Text>
      {subtitle ? <Text className="text-white/50 text-xs mt-0.5">{subtitle}</Text> : null}
    </View>
  </TouchableOpacity>
);

export default Settings;