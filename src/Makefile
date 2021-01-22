
NDK=/home/yc/Android/Sdk/ndk/21.1.6352462
TOOLCHAIN=$(NDK)/toolchains/llvm/prebuilt/linux-x86_64
TARGET=x86_64-linux-android
API=21

AR=$(TOOLCHAIN)/bin/llvm-ar
CC=$(TOOLCHAIN)/bin/$(TARGET)$(API)-clang
AS=$(CC)
CXX=$(TOOLCHAIN)/bin/$(TARGET)$(API)-clang++
LD=$(TOOLCHAIN)/bin/ld
RANLIB=$(TOOLCHAIN)/bin/llvm-ranlib
STRIP=$(TOOLCHAIN)/bin/llvm-strip

CFLAGS := \
-g \
-O3  \
-m64 \
-fPIC \
-Wdeprecated  \
-I../include -I../lib -I./kems -I./keps -I./lower_keps -I./comm -I.

LFLAGS :=  -lpqch -lcrypto -lmbedcrypto -lntl -lgmp -lgf2x -lconfig -lconfig++ -pthread -lipc  -lglog


OBJS_COMM:= \
CComm.o \
CTcpComm.o \
CKeConn.o

OBJS_KEMS:= \
CKem.o \
CRsaKem.o \
CBikeKem.o \
CFrodoKem.o \
CNewHopeKem.o \
CHqcKem.o \
CRqcKem.o \
CRolloKem.o \
CSikeKem.o \
CKyberKem.o \
CSaberKem.o \
CLacKem.o \
CNtsKem.o \
CLedaKem.o \
CNtruKem.o \
CNtruPrimeKem.o \
CRound5Kem.o \
CThreeBearsKem.o \
CCmKem.o

OBJS_KEPS:= \
CKepPhi.o \
CKepPsi.o	

OBJS_LOWER_KEPS:= \
CKep.o \
CDhKep.o \
CTwoWayKep.o \
CKemTwoWayKep.o \
CHybridTwoWayKep.o 

OBJS_OTHERS:= \
CSerializable.o \
CSharedSecretManager.o \
CGatewayConfig.o \
CKeGateWay.o


objs/%.o: kems/%.cpp
	mkdir -p objs
	$(CXX) -c -o $@ $^ $(CFLAGS)
	
	
objs/%.o: keps/%.cpp 
	mkdir -p objs
	$(CXX) -c -o $@ $^ $(CFLAGS)
	
objs/%.o: lower_keps/%.cpp
	mkdir -p objs
	$(CXX) -c -o $@ $^ $(CFLAGS)

objs/%.o: comm/%.cpp
	mkdir -p objs
	$(CXX) -c -o $@ $^ $(CFLAGS)
	
objs/%.o:  %.cpp
	mkdir -p objs
	$(CXX) -c -o $@ $^ $(CFLAGS)

OBJS:=$(addprefix objs/, $(OBJS_COMM) $(OBJS_KEPS) $(OBJS_KEMS) $(OBJS_LOWER_KEPS) $(OBJS_OTHERS))

service: $(OBJS)
	mkdir -p bin
	mkdir -p logs
	$(CXX) -c -o objs/KexService.o services/IPC_service/KexService.cpp $(CFLAGS) 
	$(AR)  rcs libKexService.a KexService.o
#	$(CXX) -c -o objs/IPC_KE_Service_Client.o services/IPC_service/IPC_KE_Service_Client.cpp $(CFLAGS)    
#	$(CXX) -c -o objs/IPC_KE_Service_Server.o services/IPC_service/IPC_KE_Service_Server.cpp $(CFLAGS)    
	$(CXX) -o bin/KexService  objs/KexService.o    $(OBJS) $(CFLAGS)  $(LFLAGS)
#	$(CXX) -o bin/IPC_KE_Service_Client  objs/IPC_KE_Service_Client.o    $(OBJS) $(CFLAGS)  $(LFLAGS)
#	$(CXX) -o bin/IPC_KE_Service_Server  objs/IPC_KE_Service_Server.o    $(OBJS) $(CFLAGS)  $(LFLAGS)
#	$(CXX) -c -o objs/test_allinone.o services/IPC_service/test_allinone.c $(CFLAGS)
#	$(CXX) -o bin/test_allinone  objs/test_allinone.o   $(CFLAGS)  $(LFLAGS)
#	$(CXX) -c -o objs/test_client.o services/IPC_service/test_client.c $(CFLAGS)
#	$(CXX) -o bin/test_client  objs/test_client.o    $(CFLAGS)  $(LFLAGS)
#	$(CXX) -c -o objs/test_server.o services/IPC_service/test_server.c $(CFLAGS)
#	$(CXX) -o bin/test_server  objs/test_server.o    $(CFLAGS)  $(LFLAGS)	
	$(CXX) -c -o objs/udp_test.o services/IPC_service/udp_test.c $(CFLAGS)
	$(CXX) -o bin/udp_test  objs/udp_test.o    $(CFLAGS)  $(LFLAGS)	
install:
	cp bin/IPC_KE_Service_Client  bin/IPC_KE_Service_Server  /usr/local/bin
	
uninstall:
	rm /usr/local/bin/IPC_KE_Service_Client  /usr/local/bin/IPC_KE_Service_Server 
	
clean:
	rm -rf bin
	rm -rf objs
	rm -rf logs
