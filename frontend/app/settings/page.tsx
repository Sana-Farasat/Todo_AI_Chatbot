import Sidebar from "@/components/SideBar";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function Settings() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <Header />
        <main className="p-8 flex-1">
          <h2 className="text-2xl font-bold mb-6 text-amber-500">Settings</h2>
          <div className="flex justify-center items-center py-20 font-bold">
            <p className=" text-amber-500">Coming soon...</p>
          </div>
        </main>
        <Footer />
      </div>
    </div>
  );
}
