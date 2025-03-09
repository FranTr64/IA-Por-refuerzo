export default function Layout({ children }) {
  return (
    <div>
      <div class="fixed top-0 left-0 h-16 w-full bg-blue-900 text-white flex justify-center items-center">
        <a href="/">Iniciar partida</a>
      </div>
      <main class="bg-gradient-to-b from-blue-400 to-green-400 h-screen w-screen flex justify-center items-center">
        {children}
      </main>
      <div class="fixed bottom-0 left-0 h-8 w-full bg-slate-900 text-white flex justify-center items-center">
      </div>
    </div>
  );
}
